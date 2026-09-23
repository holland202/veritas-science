"""Mutation operators for dependency-level verifier checks."""
from __future__ import annotations

import ast

BOUNDARY = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
}


def eligible_nodes(tree: ast.AST):
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in BOUNDARY:
            out.append(("compare", node))
    return out


def mutate_source(source: str, index: int = 0) -> str:
    tree = ast.parse(source)
    nodes = eligible_nodes(tree)
    if index >= len(nodes):
        raise IndexError("index out of range")
    kind, node = nodes[index]
    if kind == "compare":
        node.ops = [BOUNDARY[type(node.ops[0])]()]  # type: ignore[index]
    return ast.unparse(tree)


__all__ = ["eligible_nodes", "mutate_source"]
