import asyncio
from pyppeteer import launch
import frappe

async def generate_pdf(html_content, output_filename):
    browser = await launch(headless=True,handleSIGINT=False,handleSIGTERM=False,
    handleSIGHUP=False)
    page = await browser.newPage()
    
    await page.setContent(html_content)

    header_template = '''
        <div style="font-size: 10px; text-align: center; width: 100%;">
            Page No <span class="pageNumber"></span> of <span class="totalPages"></span>
        </div>
    '''
    footer_template = '''
        <div style="font-size: 10px; text-align: center; width: 100%;">
           
        </div>
    '''


    pdf = await page.pdf({'printBackground': True, 'margin': {'top': '15mm', 'right': '5mm', 'bottom': '15mm', 'left': '5mm'}, 'displayHeaderFooter': True, 'headerTemplate': header_template, 'footerTemplate': footer_template})

    await browser.close()
    return pdf

def generate_pdf_from_template(template_name, context, output_filename):
    html_content = frappe.render_template(template_name, context)
    asyncio.get_event_loop().run_until_complete(generate_pdf(html_content, output_filename))

def execute():
    template_name = "templates/print.html"
    context = {"key": "value"}
    output_filename = "{0}/outputprint.pdf".format(frappe.utils.get_files_path())
    generate_pdf_from_template(template_name, context, output_filename)


def generate_pdf_from_html(html_content, output_filename):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return asyncio.get_event_loop().run_until_complete(generate_pdf(html_content, output_filename))