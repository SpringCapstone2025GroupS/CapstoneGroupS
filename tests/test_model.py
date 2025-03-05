
from datetime import datetime
from typing import Any
from notam_fetcher.api_schema import APIResponseSuccess, Classification, ICAOTranslation, Notam, NotamType, Series


def test_all_fields_validated():
    """Test that fetch_notams correctly validates the API response"""
    valid_response_obj : dict[str, Any] = {
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
                    }
                ],
            }

    expected_notam = Notam(
        id="NOTAM_1_73849637",
        series=Series.A,
        number="A2157/24",
        type=NotamType.N,
        issued= datetime.fromisoformat("2024-10-02T19:54:00.000Z"),
        affectedFIR = "KZJX",
        selection_code="QCBLS",
        minimumFL="000",
        maximumFL="040",
        location="ZJX",
        effective_start=datetime.fromisoformat("2024-10-02T19:50:00.000Z"),
        effective_end=datetime.fromisoformat("2024-10-14T22:00:00.000Z"),
        text="ZJX AIRSPACE ADS-B, AUTO DEPENDENT SURVEILLANCE\nREBROADCAST (ADS-R), TFC INFO SER BCST (TIS-B), FLT INFO SER\nBCST (FIS-B) SER MAY NOT BE AVBL WI AN AREA DEFINED AS 49NM\nRADIUS OF 322403N0781209W.",
        classification=Classification.INTL,
        account_id="KZJX",
        last_updated=datetime.fromisoformat("2024-10-02T19:54:00.000Z"),
        icao_location = "KZJX",
        lower_limit="SFC",
        upper_limit="3999FT.",
    )

    expected_notam_translation = ICAOTranslation(
        type='ICAO',
        formatted_text="A2157/24 NOTAMN\nQ) KZJX/QCBLS////000/040/\nA) KZJX\nB) 2410021950\nC) 2410142200 EST\nE) ZJX AIRSPACE ADS-B, AUTO DEPENDENT SURVEILLANCE\nREBROADCAST (ADS-R), TFC INFO SER BCST (TIS-B), FLT INFO SER\nBCST (FIS-B) SER MAY NOT BE AVBL WI AN AREA DEFINED AS 49NM\nRADIUS OF 322403N0781209W.\nF) SFC   G) 3999FT."
    )
    
    successful_response = APIResponseSuccess.model_validate(valid_response_obj)

    assert(len(successful_response.items)==1)
    assert(successful_response.items[0].properties.coreNOTAMData.notam == expected_notam)
    assert(successful_response.items[0].properties.coreNOTAMData.notam_translation[0] == expected_notam_translation)

