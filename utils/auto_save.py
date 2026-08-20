
from __future__ import annotations
import time
import threading
import streamlit as st
from utils.config import AUTO_SAVE_INTERVAL_SECONDS

class AutoSaveThread:
    """Background thread for auto-saving."""
    
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the auto-save thread."""
        if self.thread is None or not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Stop the auto-save thread."""
        self.running = False
    
    def _run(self):
        """Auto-save loop."""
        while self.running:
            time.sleep(AUTO_SAVE_INTERVAL_SECONDS)
            try:
                if st.session_state.get("resume_dirty", False):
                    from utils.app_state import save_active_resume
                    save_active_resume()
            except:
                pass

# Global auto-save instance
_auto_save = AutoSaveThread()

def start_auto_save():
    """Start the auto-save thread."""
    _auto_save.start()

def stop_auto_save():
    """Stop the auto-save thread."""
    _auto_save.stop()
