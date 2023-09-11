import types
from pathlib import Path
import traceback

def _generate_traceback() -> types.TracebackType|None:
    tb = None
    for (frame, line_no) in traceback.walk_stack(None):
        MODULE_FOLDER = Path(__file__).parent
        frame_folder = Path(frame.f_code.co_filename).parent
        is_in_this_module = MODULE_FOLDER == frame_folder
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
