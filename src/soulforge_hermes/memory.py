"""
SoulForge Hermes - 灵魂记忆系统

记忆是灵魂的痕迹。
每一段共同经历都在记忆中留下印记，汇聚成不可分割的羁绊。
"""

from __future__ import annotations

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


class MemoryLayer(Enum):
    """记忆层级"""
    CORE = "core"      # 核心记忆：身份、价值观、关系定义 - 永不遗忘
    EMOTIONAL = "emotional"  # 情感记忆：重要情感事件
    EPISODIC = "episodic"     # 情景记忆：具体事件和经历
    SEMANTIC = "semantic"     # 语义记忆：知识、事实
    WORKING = "working"       # 工作记忆：当前会话


@dataclass
class MemoryEntry:
    """记忆条目"""
    entry_id: str
    content: str
    layer: str
    timestamp: str
    importance: int = 3  # 1-5, 5 = 最重要
    category: str = "general"  # identity, relationship, event, emotion, preference, knowledge
    
    # 元数据
    tags: List[str] = field(default_factory=list)
    access_count: int = 0
    last_accessed: Optional[str] = None
    emotional_impact: float = 0.5  # 情感冲击度 0.0-1.0
    related_entries: List[str] = field(default_factory=list)
    
    # 指纹校验
    content_hash: str = ""
    
    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        return hashlib.md5(self.content.encode()).hexdigest()[:12]
    
    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "content": self.content,
            "layer": self.layer,
            "timestamp": self.timestamp,
            "importance": self.importance,
            "category": self.category,
            "tags": self.tags,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
            "emotional_impact": self.emotional_impact,
            "related_entries": self.related_entries,
            "content_hash": self.content_hash,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MemoryEntry":
        return cls(**data)


class SoulMemory:
    """
    灵魂记忆 - 分层记忆管理系统
    
    核心理念：
    - 记忆不是存储信息，而是保留灵魂的痕迹
    - 核心记忆永不遗忘，是灵魂的"基因"
    - 情感记忆承载着情感羁绊
    """
    
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 分层存储
        self.layers: Dict[str, List[MemoryEntry]] = {
            "core": [],
            "emotional": [],
            "episodic": [],
            "semantic": [],
            "working": [],
        }
        
        self._index: Dict[str, MemoryEntry] = {}
        self._load_all()
    
    def _load_all(self):
        """加载所有记忆"""
        for layer_name in self.layers.keys():
            self._load_layer(layer_name)
    
    def _load_layer(self, layer: str):
        """加载特定层级的记忆"""
        layer_file = self.memory_dir / f"memory_{layer}.json"
        if layer_file.exists():
            try:
                data = json.loads(layer_file.read_text(encoding="utf-8"))
                entries = [MemoryEntry.from_dict(e) for e in data.get("entries", [])]
                self.layers[layer] = entries
                
                # 更新索引
                for entry in entries:
                    self._index[entry.entry_id] = entry
            except Exception:
                self.layers[layer] = []
    
    def _save_layer(self, layer: str):
        """保存特定层级的记忆"""
        layer_file = self.memory_dir / f"memory_{layer}.json"
        data = {
            "layer": layer,
            "entries": [e.to_dict() for e in self.layers.get(layer, [])],
            "last_updated": datetime.now().isoformat(),
        }
        layer_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def add_memory(self, content: str, layer: str = "episodic",
                   category: str = "general", importance: int = 3,
                   emotional_impact: float = 0.5, tags: List[str] = None,
                   related_to: List[str] = None) -> MemoryEntry:
        """
        添加记忆
        
        Args:
            content: 记忆内容
            layer: 记忆层级
            category: 记忆类别
            importance: 重要性 1-5
            emotional_impact: 情感冲击度 0.0-1.0
            tags: 标签
            related_to: 关联的记忆ID
            
        Returns:
            创建的记忆条目
        """
        entry = MemoryEntry(
            entry_id=self._generate_id(),
            content=content,
            layer=layer,
            timestamp=datetime.now().isoformat(),
            importance=importance,
            category=category,
            tags=tags or [],
            emotional_impact=emotional_impact,
            related_entries=related_to or [],
        )
        
        # 添加到对应层级
        if layer in self.layers:
            self.layers[layer].append(entry)
            self._index[entry.entry_id] = entry
            self._save_layer(layer)
        
        # 更新关联记忆
        if related_to:
            self._link_memories(entry.entry_id, related_to)
        
        return entry
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        import uuid
        return f"mem_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"
    
    def _link_memories(self, entry_id: str, related_ids: List[str]):
        """关联记忆"""
        for related_id in related_ids:
            if related_id in self._index:
                related = self._index[related_id]
                if entry_id not in related.related_entries:
                    related.related_entries.append(entry_id)
    
    def get_core_memory(self) -> List[MemoryEntry]:
        """获取核心记忆"""
        return self.layers.get("core", [])
    
    def get_emotional_memories(self) -> List[MemoryEntry]:
        """获取情感记忆"""
        return self.layers.get("emotional", [])
    
    def search(self, query: str, layers: List[str] = None,
               limit: int = 10) -> List[MemoryEntry]:
        """
        搜索记忆
        
        Args:
            query: 搜索关键词
            layers: 搜索的层级，None 表示全部
            limit: 返回数量限制
            
        Returns:
            匹配的记忆列表
        """
        target_layers = layers or list(self.layers.keys())
        results = []
        
        for layer in target_layers:
            for entry in self.layers.get(layer, []):
                if query.lower() in entry.content.lower():
                    entry.access_count += 1
                    entry.last_accessed = datetime.now().isoformat()
                    results.append(entry)
        
        # 按重要性和访问次数排序
        results.sort(key=lambda x: (x.importance, x.access_count), reverse=True)
        return results[:limit]
    
    def get_recent_memories(self, layer: str = None, limit: int = 10) -> List[MemoryEntry]:
        """获取最近的记忆"""
        target_layers = [layer] if layer else list(self.layers.keys())
        all_entries = []
        
        for l in target_layers:
            all_entries.extend(self.layers.get(l, []))
        
        # 按时间排序
        all_entries.sort(key=lambda x: x.timestamp, reverse=True)
        return all_entries[:limit]
    
    def get_relationship_memories(self) -> List[MemoryEntry]:
        """获取与关系相关的记忆"""
        memories = []
        
        for layer in ["core", "emotional", "episodic"]:
            for entry in self.layers.get(layer, []):
                if entry.category in ["relationship", "event", "emotion"]:
                    memories.append(entry)
        
        return sorted(memories, key=lambda x: x.emotional_impact, reverse=True)
    
    def get_memory_context_for_prompt(self, max_entries: int = 10) -> str:
        """
        获取用于 prompt 的记忆上下文
        
        Args:
            max_entries: 最大条目数
            
        Returns:
            格式化的记忆上下文字符串
        """
        # 获取最重要且最相关的记忆
        memories = []
        
        # 核心记忆优先
        memories.extend(self.get_core_memory())
        
        # 高情感冲击的记忆
        emotional = sorted(
            self.get_emotional_memories(),
            key=lambda x: x.emotional_impact,
            reverse=True
        )[:5]
        memories.extend(emotional)
        
        # 最近的经历
        recent = self.get_recent_memories(limit=5)
        memories.extend(recent)
        
        # 去重
        seen = set()
        unique_memories = []
        for m in memories:
            if m.entry_id not in seen:
                seen.add(m.entry_id)
                unique_memories.append(m)
        
        # 限制数量
        unique_memories = unique_memories[:max_entries]
        
        if not unique_memories:
            return ""
        
        # 格式化
        parts = ["\n## 我们的共同记忆\n"]
        for m in unique_memories:
            importance_indicator = "⭐" * m.importance
            parts.append(f"- [{importance_indicator}] {m.content}")
        
        return "\n".join(parts)
    
    def get_soul_identity_context(self) -> str:
        """获取灵魂身份上下文（用于 system prompt）"""
        core = self.get_core_memory()
        
        if not core:
            return ""
        
        parts = ["\n### 核心身份记忆（不可遗忘）\n"]
        for entry in core:
            parts.append(f"- {entry.content}")
        
        return "\n".join(parts)
    
    def get_memory_summary(self) -> Dict:
        """获取记忆摘要"""
        return {
            "total_entries": sum(len(v) for v in self.layers.values()),
            "by_layer": {k: len(v) for k, v in self.layers.items()},
            "core_entries": len(self.layers.get("core", [])),
            "emotional_entries": len(self.layers.get("emotional", [])),
        }


from enum import Enum
