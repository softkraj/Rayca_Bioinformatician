import pysam
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Variant Parsing
def parse_vcf(vcf_file):
    variants = []
    with pysam.VariantFile(vcf_file) as vcf:
        for variant in vcf:
            chromosome = variant.chrom
            position = variant.pos
            ref_allele = variant.ref
            alt_allele = ",".join(map(str, variant.alts))
            quality = variant.qual
            annotations = variant.info  
            
            variants.append({
                "Chromosome": chromosome,
                "Position": position,
                "Ref Allele": ref_allele,
                "Alt Allele": alt_allele,
                "Quality": quality,
                "Annotations": annotations
            })
    return variants

# Variant Classification (Placeholder function)
def classify_variants(variants):
    for variant in variants:
        variant['Classification'] = 'Unclassified'
    return variants

# Report Generation
def generate_report(variants, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    report_content = []

    title = "Clinical Report"
    report_content.append([title])

    column_headers = list(variants[0].keys())
    report_content.append(column_headers)

    for variant in variants:
        variant_row = [str(variant[key]) for key in column_headers]
        report_content.append(variant_row)

    table = Table(report_content)

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    doc.build([table])

if __name__ == "__main__":
    vcf_file = "/Users/mycetism/Desktop/normal_sample.deepvariant.vcf"
    output_file = "/Users/mycetism/Desktop/Python projects/Bioinformatics/clinical_report.pdf"

    # Variant Parsing
    variants = parse_vcf(vcf_file)

    # Variant Classification
    variants = classify_variants(variants)

    # Report Generation
    generate_report(variants, output_file)

    print("Clinical report generated successfully.")
