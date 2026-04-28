import os
from typing import List, Dict
import yaml

class NovelRepository:
    def __init__(self, data_path: str = "/workspaces/Nature-AI/data/novels"):
        self.data_path = data_path

    def list_novels(self) -> List[Dict]:
        novels = []
        for file in os.listdir(self.data_path):
            if file.endswith('.md'):
                path = os.path.join(self.data_path, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 解析frontmatter
                    if content.startswith('---'):
                        end = content.find('---', 3)
                        if end != -1:
                            frontmatter = yaml.safe_load(content[3:end])
                            novels.append({
                                'id': file.replace('.md', ''),
                                'title': frontmatter.get('title', file),
                                'author': frontmatter.get('author', '未知'),
                                'genre': frontmatter.get('genre', '未知'),
                                'summary': frontmatter.get('summary', ''),
                                'content': content[end+3:].strip()
                            })
        return novels

    def get_novel(self, novel_id: str) -> Dict:
        path = os.path.join(self.data_path, f"{novel_id}.md")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    end = content.find('---', 3)
                    if end != -1:
                        frontmatter = yaml.safe_load(content[3:end])
                        return {
                            'id': novel_id,
                            'title': frontmatter.get('title', novel_id),
                            'author': frontmatter.get('author', '未知'),
                            'genre': frontmatter.get('genre', '未知'),
                            'summary': frontmatter.get('summary', ''),
                            'content': content[end+3:].strip()
                        }
        return None