from io import BytesIO

import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now


def df_to_excel_response(df: pd.DataFrame | None, base_filename: str):
    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    df_out = df.copy().reset_index().rename(columns={"index": "Period"})

    timestamp = now().strftime("%Y%m%d-%H%M")
    filename = f"{base_filename}_{timestamp}.xlsx"

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df_out.to_excel(writer, index=False, sheet_name="Data")
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
