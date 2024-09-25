from io import BytesIO
from django.utils import timezone
from django.utils.text import slugify
from django.http.response import FileResponse


datetime_format = "dd/mm/yyyy hh:mm:ss"
date_format = "dd/mm/yyyy"
engine = "xlsxwriter"

try:

    import pandas as pd

    def exportar_para_excel(title, columns, rows):
        """
        Retornar uma response pronta para retornar ao usuário.
        Para usar é necessário instalar a biblioteca pandas e a biblioteca XlsxWriter
        """

        df = pd.DataFrame(rows, columns=columns)
        filename = f'{timezone.now().strftime("%Y-%m-%d")}-{slugify(title)}.xlsx'
        file = BytesIO()
        with pd.ExcelWriter(
            file,
            engine=engine,
            datetime_format=datetime_format,
            date_format=date_format,
        ) as writer:
            df.to_excel(writer, sheet_name=title, index=False)
        file.seek(0)
        return FileResponse(file, filename=filename)

except ImportError:
    pass
