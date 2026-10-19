"""Extract text and tables from an HWP 5 file into Markdown-like text.

Usage: python -I hwp2md.py input.hwp output.md
"""
import struct
import sys
import zlib

import olefile

PARA_HEADER, PARA_TEXT, CTRL_HEADER, LIST_HEADER, TABLE = 66, 67, 71, 72, 77
EXTENDED = {1, 2, 3, 11, 12, 14, 15, 16, 17, 18, 21, 22, 23}
INLINE = {4, 5, 6, 7, 8, 9, 19, 20}


class Node:
    def __init__(self, tag, level, data):
        self.tag, self.level, self.data, self.children = tag, level, data, []


def read_records(data):
    pos, out = 0, []
    while pos + 4 <= len(data):
        (h,) = struct.unpack_from("<I", data, pos)
        pos += 4
        tag, level, size = h & 0x3FF, (h >> 10) & 0x3FF, (h >> 20) & 0xFFF
        if size == 0xFFF:
            (size,) = struct.unpack_from("<I", data, pos)
            pos += 4
        out.append(Node(tag, level, data[pos:pos + size]))
        pos += size
    return out


def build_tree(records):
    root = Node(None, -1, b"")
    stack = [root]
    for r in records:
        while stack[-1].level >= r.level:
            stack.pop()
        stack[-1].children.append(r)
        stack.append(r)
    return root


def para_text(data):
    units = struct.unpack(f"<{len(data) // 2}H", data[: len(data) // 2 * 2])
    out, i = [], 0
    while i < len(units):
        c = units[i]
        if c in EXTENDED or c in INLINE:
            if c == 9:
                out.append("\t")
            i += 8
            continue
        if c == 10:
            out.append(" / ")
        elif c >= 32:
            out.append(chr(c))
        i += 1
    return "".join(out).strip()


def render_table(ctrl):
    cells = []
    cur = None
    seen_table = False
    for ch in ctrl.children:
        if ch.tag == TABLE:
            seen_table = True
            continue
        if not seen_table:
            continue  # caption list comes before the TABLE record
        if ch.tag == LIST_HEADER:
            d = ch.data
            col, row, cspan, rspan = struct.unpack_from("<HHHH", d, 8)
            cur = {"row": row, "col": col, "cs": max(cspan, 1), "rs": max(rspan, 1), "nodes": []}
            cells.append(cur)
            cur["nodes"].extend(ch.children)
        elif cur is not None and ch.tag == PARA_HEADER:
            cur["nodes"].append(ch)
    if not cells:
        return []
    nrows = max(c["row"] + c["rs"] for c in cells)
    ncols = max(c["col"] + c["cs"] for c in cells)
    if nrows > 400 or ncols > 60:
        return [f"[table with bad dims {nrows}x{ncols}]"]
    grid = [[""] * ncols for _ in range(nrows)]
    nested = []
    for c in cells:
        lines = []
        for n in c["nodes"]:
            lines.extend(render_para(n))
        kept, block, depth = [], [], 0
        for l in lines:
            if l.startswith("<<TABLE"):
                depth += 1
            if depth:
                block.append(l)
                if l == "<<END TABLE>>":
                    depth -= 1
                    if depth == 0:
                        nested.extend(["(nested table in cell r%d c%d)" % (c["row"], c["col"])] + block + [""])
                        kept.append("[nested table below]")
                        block = []
            else:
                kept.append(l)
        text = " / ".join(l for l in kept if l).replace("|", "/")
        grid[c["row"]][c["col"]] = text
        for r in range(c["row"], c["row"] + c["rs"]):
            for k in range(c["col"], c["col"] + c["cs"]):
                if (r, k) != (c["row"], c["col"]):
                    grid[r][k] = "〃"
    out = ["", f"<<TABLE {nrows}x{ncols}>>"]
    for r in grid:
        out.append("| " + " | ".join(r) + " |")
    out.append("<<END TABLE>>")
    out.append("")
    return out + nested


def render_para(node, nested_out=None):
    out = []
    if node.tag != PARA_HEADER:
        return out
    for ch in node.children:
        if ch.tag == PARA_TEXT:
            t = para_text(ch.data)
            if t:
                out.append(t)
        elif ch.tag == CTRL_HEADER:
            cid = ch.data[:4][::-1]
            if cid == b"tbl ":
                out.extend(render_table(ch))
            else:
                # Text boxes and other containers can hold paragraphs too.
                for sub in walk_paras(ch):
                    out.extend(render_para(sub))
    return out


def walk_paras(node):
    for ch in node.children:
        if ch.tag == PARA_HEADER:
            yield ch
        elif ch.tag == LIST_HEADER or ch.tag not in (CTRL_HEADER,):
            yield from walk_paras(ch)


def main(src, dst):
    ole = olefile.OleFileIO(src)
    header = ole.openstream("FileHeader").read()
    (props,) = struct.unpack_from("<I", header, 36)
    compressed, encrypted, distribution = props & 1, props & 2, props & 4
    if encrypted or distribution:
        raise SystemExit(f"encrypted={encrypted} distribution={distribution}")
    sections = sorted(
        (e for e in ole.listdir() if e[0] == "BodyText"), key=lambda e: int(e[1][7:])
    )
    lines = []
    for e in sections:
        data = ole.openstream(e).read()
        if compressed:
            data = zlib.decompress(data, -15)
        tree = build_tree(read_records(data))
        for n in tree.children:
            lines.extend(render_para(n))
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
