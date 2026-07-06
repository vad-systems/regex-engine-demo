from .ast_nodes import ASTNode, Literal, Concatenation, Alternation, Star, Plus, Optional, Repetition, CharacterGroup, \
    BinaryOp, UnaryOp


def ast_to_dot(node: ASTNode) -> str:
    dot = ["digraph AST {", "  node [fontname=\"Arial\"];"]
    node_id = 0

    def traverse(curr_node: ASTNode):
        nonlocal node_id
        curr_id = node_id
        node_id += 1

        label = curr_node.__class__.__name__
        if isinstance(curr_node, Literal):
            label += f" ('{curr_node.char}')"
        elif isinstance(curr_node, Repetition):
            label += f" ({curr_node.min}, {curr_node.max})"

        dot.append(f'  {curr_id} [label="{label}"];')

        if isinstance(curr_node, BinaryOp):
            left_id = traverse(curr_node.left)
            right_id = traverse(curr_node.right)
            dot.append(f'  {curr_id} -> {left_id};')
            dot.append(f'  {curr_id} -> {right_id};')
        elif isinstance(curr_node, UnaryOp):
            expr_id = traverse(curr_node.expression)
            dot.append(f'  {curr_id} -> {expr_id};')
        elif isinstance(curr_node, CharacterGroup):
            pass  # Leaf node in AST visualization

        return curr_id

    traverse(node)
    dot.append("}")
    return "\n".join(dot)


def ast_to_ascii(node: ASTNode, indent: str = "") -> str:
    if isinstance(node, Literal):
        return f"{indent}Literal('{node.char}')"
    elif isinstance(node, CharacterGroup):
        return f"{indent}CharacterGroup(\"\".join(node.chars))"
    elif isinstance(node, Concatenation):
        return f"{indent}Concatenation\n{ast_to_ascii(node.left, indent + '  ')} \n{ast_to_ascii(node.right, indent + '  ')}"
    elif isinstance(node, Alternation):
        return f"{indent}Alternation\n{ast_to_ascii(node.left, indent + '  ')} \n{ast_to_ascii(node.right, indent + '  ')}"
    elif isinstance(node, (Star, Plus, Optional, Repetition)):
        return f"{indent}{node.__class__.__name__}\n{ast_to_ascii(node.expression, indent + '  ')}"
    return f"{indent}{type(node).__name__}"
