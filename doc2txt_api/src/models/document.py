import os
import shutil
from functools import cached_property
from typing import ClassVar
from uuid import UUID, uuid4
from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_validator,
    )
from utils.my_logging import debug
from utils.functions import (
    decode_bs64_to_file,
    subprocess_mgr,
)
from utils.exceptions import LibreOfficeConversion




class Document(BaseModel):
    root_path: ClassVar[str] = '/tmp/doc2txt'
    supported_exts_doc: ClassVar[tuple[str]] = ('.pdf', '.doc', '.docx', '.odt', '.rtf')
    supported_exts_img: ClassVar[tuple[str]] = ('.jpg', '.png')

    id: UUID = Field(default_factory=uuid4, frozen=True)
    f_name: str = Field(min_length=3, pattern=r"[^\\]*\.\w+$", frozen=False)
    content: str = Field(min_length=1, repr=False)
    source: str = Field(min_length=1, frozen=True)


    @field_validator('f_name')
    @classmethod
    def name_must_contain_valid_extension(cls, v: str):
        v = v.lower()
        supported_exts = cls.supported_exts_doc + cls.supported_exts_img
        if not any(x for x in supported_exts if x in v):
            raise ValueError('extension not supported')
        return v


    @computed_field
    @cached_property
    def extension(self) -> str:
        return f".{self.f_name.split('.')[-1]}"


    @computed_field
    @cached_property
    def is_image(self) -> bool:
        return self.extension in self.supported_exts_img


    @computed_field
    @cached_property
    def paths(self) -> dict:
        uid_path = os.path.join(self.root_path, str(self.id))
        name_pdf = self.f_name.replace(self.extension, '.pdf')
        name_html = self.f_name.replace(self.extension, '.html')

        return {
            'uid': uid_path,
            'file': os.path.join(uid_path, self.f_name),
            'file_pdf': os.path.join(uid_path, name_pdf),
            'file_html': os.path.join(uid_path, name_html),
            'pngs': os.path.join(uid_path, 'pngs'),
        }


    def create_paths(self) -> None:
        if not os.path.isdir(self.root_path):
            os.mkdir(self.root_path)
        os.mkdir(self.paths['uid'])


    def remove_path(self) -> None:
        shutil.rmtree(self.paths['uid'])


    def save_doc(self) -> None:
        self.create_paths()
        decode_bs64_to_file(self.paths['file'], self.content)
        del self.content


    @debug
    def doc_to_pdf(self, c: int = 0) -> None:
        timeout = 4
        retries = 10
        f_out = self.paths['file_pdf']

        cmd = [
            '/usr/bin/lowriter',
            '--headless',
            '--convert-to',
            'pdf',
            '--outdir',
            self.paths['uid'],
            self.paths['file']
        ]
        subprocess_mgr(cmd, 'Libreoffice', timeout)

        if c < retries and not os.path.isfile(f_out):
            c += 1
            self.doc_to_pdf(c)

        if not os.path.isfile(f_out):
            raise LibreOfficeConversion(self.extension)

