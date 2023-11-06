import pyinstaller_versionfile

from const import NAME, VERSION,AUTHOR,AUTHOR_EMAIL, DESCRIPTION, COMPANY

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version=f"{VERSION}",
    company_name=COMPANY,
    file_description=DESCRIPTION,
    internal_name=COMPANY,
    legal_copyright=f"© {AUTHOR}. All rights reserved.",
    original_filename=f"{NAME}.exe",
    product_name=f"{NAME}"
)