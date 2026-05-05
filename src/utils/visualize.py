try:
    from langgraph.graph.state import CompiledGraph
except ImportError:
    try:
        from langgraph.graph import CompiledStateGraph as CompiledGraph
    except ImportError:
        CompiledGraph = object

try:
    from langchain_core.runnables.graph import MermaidDrawMethod
except ImportError:
    MermaidDrawMethod = None


def save_graph_as_png(app, output_file_path) -> None:
    if MermaidDrawMethod is None:
        raise ImportError("MermaidDrawMethod not available in this version of langchain_core")
    png_image = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
    file_path = output_file_path if len(output_file_path) > 0 else "graph.png"
    with open(file_path, "wb") as f:
        f.write(png_image)