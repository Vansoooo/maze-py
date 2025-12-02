"""Utilities for capturing maze animation timelines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal

Phase = Literal["generate", "solve"]


@dataclass(slots=True)
class AnimationEvent:
    phase: Phase
    event: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"phase": self.phase, "event": self.event, **self.payload}


class AnimationRecorder:
    """Collects generator and solver events for later playback/export."""

    def __init__(self) -> None:
        self._events: List[AnimationEvent] = []

    def record(self, phase: Phase, event: str, **payload: Any) -> None:
        self._events.append(AnimationEvent(phase=phase, event=event, payload=payload))

    @property
    def events(self) -> List[AnimationEvent]:
        return list(self._events)

    def to_serializable(self) -> List[Dict[str, Any]]:
        return [evt.to_dict() for evt in self._events]

