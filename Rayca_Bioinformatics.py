import os
import vcfpy
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Function to parse VCF file and extract variant information
def parse_vcf(vcf_file):
    variants = []
    reader = vcfpy.Reader.from_path(vcf_file)
    for record in reader:
        variant_info = {
            'Chromosome': record.CHROM,
            'Position': record.POS,
            'Reference Allele': record.REF,
            'Alternate Allele': record.ALT[0].value,
            'Variant Quality': record.QUAL,
            'Filter Status': record.FILTER,
            'ACMG Classification': record.ACMG
            # Add more fields as needed
        }
        variants.append(variant_info)
    return variants

def classify_variants(variants):
    classifications = ['Pathogenic', 'Likely Pathogenic', 'Benign', 'Likely Benign', 'Uncertain Significance']
    return classifications

# Function to generate PDF report
def generate_pdf_report(patient_info, variants):
    pdf_filename = 'clinical_report.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Patient information table
    patient_data = [
        ['Patient ID', patient_info['Patient ID']],
        ['Date of Birth', patient_info['Date of Birth']],
        ['Gender', patient_info['Gender']],
        ['Ethnicity', patient_info['Ethnicity']]
    ]
    patient_table = Table(patient_data)
    patient_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                       ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                       ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    
    # Variants table
    variant_data = [['Chromosome', 'Position', 'Reference Allele', 'Alternate Allele', 'Quality', 'Filter', 'ACMG Classification']]
    for variant in variants:
        variant_data.append([
            variant['Chromosome'],
            variant['Position'],
            variant['Reference Allele'],
            variant['Alternate Allele'],
            variant['Quality'],
            variant['Filter'],
            variant.get('ACMG Classification', 'Pathogenic', 'Likely Pathogenic', 'Benign', 'Likely Benign', 'Uncertain Significance')  # Add ACMG classification if available
        ])
    variant_table = Table(variant_data)
    variant_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                       ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                       ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Build PDF
    doc.build([patient_table, variant_table])

    print(f"PDF report generated: {os.path.abspath(pdf_filename)}")  # Fix indentation

# Main function
def main():
    vcf_file = "/Users/mycetism/Desktop/Python projects/Bioinformatics/normal_sample.deepvariant.vcf.gz"
