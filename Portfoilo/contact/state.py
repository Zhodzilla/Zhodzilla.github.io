from typing import List
import asyncio
import reflex as rx

from sqlmodel import select
from .model import ContactEntryModel

class ContactState(rx.State):
    form_data: dict ={}
    entries: List["ContactEntryModel"] = []
    did_submit: bool = False

    @rx.var
    def thank_you(self) -> str:
        first_name = self.form_data.get("first_name") or ("")
        return f"Thank you {first_name}!"

    async def handle_submit(self, form_data: dict):

        print(form_data)
        self.form_data = form_data
        data = {}
        for k,v in form_data.items():
            if v == "" or v is None:
                continue
            data[k] = v

        with rx.session() as session:
            db_entry = ContactEntryModel(
                **data
            )
            session.add(db_entry)
            session.commit()
            self.did_submit = True
            yield

        await asyncio.sleep(2)
        self.did_submit = False
        yield

    def list_entries(self):
        with rx.session() as session:
            entries = session.exec(
                select(ContactEntryModel)
            ).all()
            self.entries = entries