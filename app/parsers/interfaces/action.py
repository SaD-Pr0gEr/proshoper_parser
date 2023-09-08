from dataclasses import dataclass
from pathlib import Path

import requests


@dataclass
class ActionPhoto:
    PHOTO_ID: int
    PHOTO_LINK: str
    PHOTO_LOCAL_PATH: str | None = None

    @property
    def photo_format(self) -> str:
        return self.PHOTO_LINK.split('.')[-1]

    def load_photo(self, photo_dir: Path, action_id: int) -> str:
        photo_path = f'{action_id}/{self.PHOTO_ID}.{self.photo_format}'
        self.PHOTO_LOCAL_PATH = str(photo_dir / photo_path)
        response = requests.get(self.PHOTO_LINK)
        with open(self.PHOTO_LOCAL_PATH, 'wb') as file:
            file.write(response.content)
        return str(photo_dir).split('/')[-1] + f'/{photo_path}'
