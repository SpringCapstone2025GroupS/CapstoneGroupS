"""
This file contains the Pydantic models used to parse the JSON returned from the API

Example response:
{
    "pageSize": 50,
    "pageNum": 1,
    "totalCount": 2,
    "totalPages": 1,
    "items": [
        {
            "type": "Feature",
            "properties": {
                "coreNOTAMData": {
                    "notamEvent": {"scenario": "6000"},
                    "notam": {
                        "id": "NOTAM_1_73849637",
                        "series": "A",
                        "number": "A2157/24",
                        "type": "N",
                        "issued": "2024-10-02T19:54:00.000Z",
                        "affectedFIR": "KZJX",
                        "selectionCode": "QCBLS",
                        "minimumFL": "000",
                        "maximumFL": "040",
                        "location": "ZJX",
                        "effectiveStart": "2024-10-02T19:50:00.000Z",
                        "effectiveEnd": "2024-10-14T22:00:00.000Z",
                        "text": "ZJX AIRSPACE ADS-B, AUTO DEPENDENT SURVEILLANCE\nREBROADCAST (ADS-R), TFC INFO SER BCST (TIS-B), FLT INFO SER\nBCST (FIS-B) SER MAY NOT BE AVBL WI AN AREA DEFINED AS 49NM\nRADIUS OF 322403N0781209W.",
                        "classification": "INTL",
                        "accountId": "KZJX",
                        "lastUpdated": "2024-10-02T19:54:00.000Z",
                        "icaoLocation": "KZJX",
                        "lowerLimit": "SFC",
                        "upperLimit": "3999FT.",
                    },
                    "notamTranslation": [
                        {
                            "type": "ICAO",
                            "formattedText": "A2157/24 NOTAMN\nQ) KZJX/QCBLS////000/040/\nA) KZJX\nB) 2410021950\nC) 2410142200 EST\nE) ZJX AIRSPACE ADS-B, AUTO DEPENDENT SURVEILLANCE\nREBROADCAST (ADS-R), TFC INFO SER BCST (TIS-B), FLT INFO SER\nBCST (FIS-B) SER MAY NOT BE AVBL WI AN AREA DEFINED AS 49NM\nRADIUS OF 322403N0781209W.\nF) SFC   G) 3999FT.",
                        }
                    ],
                }
            },
            "geometry": {"type": "GeometryCollection"},
        },
        {
            "type": "Point",
            "geometry": {"type": "Point", "coordinates": [0]},
            "properties": {"name": "Dinagat Islands"},
        },
    ],
}
"""


from datetime import datetime
from typing import Any, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, alias_generators


class NotamTranslationObject(BaseModel):
    pass


class LocalFormatTranslationObject(NotamTranslationObject):
    type: Literal["LOCAL_FORMAT"]
    simple_text: str = Field(alias="simpleText")

class ICAOTranslationObject(NotamTranslationObject):
    type: Literal["ICAO"]
    formatted_text: str = Field(alias="formattedText")


class Notam(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel
    )
    
    id: str
    number: str
    type: str
    issued: datetime
    selection_code: Optional[str]
    location: str
    effective_start: datetime
    effective_end: datetime | str
    text: str
    classification: str
    account_id: str
    last_updated: datetime
    icao_location: str


class NotamEvent(BaseModel):
    scenario: str


class CoreNotamData(BaseModel):
    notamEvent: NotamEvent
    notam: Notam
    notamTranslation: list[ICAOTranslationObject | LocalFormatTranslationObject]


class NotamApiItemProperties(BaseModel):
    coreNOTAMData: CoreNotamData


class ResponseItem(BaseModel):
    pass


class OtherResponseItem(ResponseItem):
    type: str
    properties: dict[str, Any]
    geometry: dict[str, Any]


class NotamApiItem(ResponseItem):
    type: Literal["Feature"]
    properties: NotamApiItemProperties
    geometry: dict[str, Any]


class NotamAPIResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel
    )
    page_size: int
    page_num: int
    total_count: int
    total_pages: int
    items: list[NotamApiItem | OtherResponseItem]
