import pandas as pd
import os
from pathlib import Path
from docxtpl import DocxTemplate
from django.conf import settings
from .models import *

def generate_files(template_path, data_path):      #these should be filepaths
    # template_path = os.path.join(settings.MEDIA_ROOT, template_path)
    template_path = settings.MEDIA_ROOT.joinpath(template_path)
    # data_path = os.path.join(settings.MEDIA_ROOT, data_path)
    data_path = settings.MEDIA_ROOT.joinpath(data_path)


    data_df = pd.read_csv(data_path, header=0)
    for index, row in data_df.iterrows():
        context = {}
        for column in data_df.columns:
            var = row[column]
            context[column] = var

        template = DocxTemplate(template_path)
        template.render(context)
        template.save(settings.MEDIA_ROOT.joinpath(f"files\generated\doc-{index}.docx"))

        f = File(name=index, filepath=f"files\generated\doc-{index}.docx")
        f.save()



