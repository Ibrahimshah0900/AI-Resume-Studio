
from __future__ import annotations
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

class ResumeManager:
    """Manage multiple resume drafts with localStorage and file persistence."""
    
    def __init__(self, storage_path: str | Path = None):
        if storage_path is None:
            storage_path = Path.cwd() / "AI-Resume-Studio" / "data" / "resume_drafts"
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._drafts_file = self.storage_path / "drafts.json"
        self._load_drafts()
    
    def _load_drafts(self) -> None:
        """Load drafts from JSON file."""
        if self._drafts_file.exists():
            try:
                with open(self._drafts_file, 'r') as f:
                    self.drafts = json.load(f)
            except:
                self.drafts = {}
        else:
            self.drafts = {}
    
    def _save_drafts(self) -> None:
        """Save drafts to JSON file."""
        with open(self._drafts_file, 'w') as f:
            json.dump(self.drafts, f, indent=2, ensure_ascii=False)
    
    def create_draft(self, name: str, data: Dict[str, Any]) -> str:
        """Create a new resume draft."""
        draft_id = str(uuid.uuid4())
        self.drafts[draft_id] = {
            "id": draft_id,
            "name": name,
            "data": data,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "version": 1
        }
        self._save_drafts()
        return draft_id
    
    def update_draft(self, draft_id: str, data: Dict[str, Any], name: str = None) -> bool:
        """Update an existing draft."""
        if draft_id not in self.drafts:
            return False
        
        if name:
            self.drafts[draft_id]["name"] = name
        
        self.drafts[draft_id]["data"] = data
        self.drafts[draft_id]["updated_at"] = datetime.now().isoformat()
        self.drafts[draft_id]["version"] += 1
        self._save_drafts()
        return True
    
    def get_draft(self, draft_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific draft."""
        return self.drafts.get(draft_id)
    
    def list_drafts(self) -> List[Dict[str, Any]]:
        """List all drafts."""
        return sorted(
            [{"id": k, **v} for k, v in self.drafts.items()],
            key=lambda x: x["updated_at"],
            reverse=True
        )
    
    def delete_draft(self, draft_id: str) -> bool:
        """Delete a draft."""
        if draft_id in self.drafts:
            del self.drafts[draft_id]
            self._save_drafts()
            return True
        return False
    
    def duplicate_draft(self, draft_id: str, new_name: str) -> Optional[str]:
        """Duplicate an existing draft."""
        if draft_id not in self.drafts:
            return None
        
        draft = self.drafts[draft_id]
        new_id = str(uuid.uuid4())
        self.drafts[new_id] = {
            "id": new_id,
            "name": new_name,
            "data": draft["data"].copy(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "version": 1
        }
        self._save_drafts()
        return new_id
    
    def export_draft(self, draft_id: str, format: str = "json") -> Optional[str]:
        """Export a draft to a specific format."""
        draft = self.get_draft(draft_id)
        if not draft:
            return None
        
        if format == "json":
            return json.dumps(draft, indent=2)
        return None
