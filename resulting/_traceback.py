import types
from pathlib import Path
import traceback

MODULE_FOLDER = str(Path(__file__).parent)
def _generate_traceback() -> types.TracebackType|None:
    tb = None
    for (frame, line_no) in traceback.walk_stack(None):
        stack_file = frame.f_code.co_filename
        is_in_this_module = stack_file.startswith(MODULE_FOLDER)
        if is_in_this_module:
            continue

        if _is_frame_in_debugger(frame):
            continue

        tb = types.TracebackType(tb, frame, frame.f_lasti, frame.f_lineno)

    return tb


def _is_frame_in_debugger(frame: types.FrameType) -> bool:
    if frame.f_trace is not None:
        return True

    filename = frame.f_globals.get("__file__", "")
    if "pydevd" in filename or "debugpy" in filename:
        return True

    return False
