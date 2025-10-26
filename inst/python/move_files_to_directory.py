import os
import shutil


def add_tsv_extension(original_list):
    return [item + '.tsv' for item in original_list]


list2 = ['ADAM10', 'CASK', 'MAPK12', 'LLGL1', 'GRIN2A', 'UBE3A', 'GRIN2B', 'PTEN', 'GRIA1', 'ADAM22', 'TJAP1', 'KCNA4',
         'NBEA', 'LRFN2', 'SYNGAP1', 'CACNG2', 'NLGN2', 'ERBB4', 'GRIN1', 'NLGN1', 'GRIK2', 'GRM1', 'GRM5', 'NLGN4X',
         'ARHGEF7', 'CTTN', 'NLGN3', 'NRXN1']
files_to_move_to2layer = add_tsv_extension(list2)

# 'CDC42.tsv',, 'WHRN.tsv', 'NLGN4Y.tsv'
files_to_move_to3layer = ['ARHGEF6.tsv', 'PAK2.tsv', 'PAK3.tsv', 'PAK1.tsv', 'GIT2.tsv', 'GIT1.tsv',
                          'CBL.tsv', 'SCRIB.tsv', 'SRC.tsv', 'CACNB4.tsv', 'CACNG1.tsv', 'GRIA4.tsv', 'GRIA2.tsv',
                          'SHISA9.tsv', 'GRIA3.tsv', 'APBA1.tsv', 'LIN7C.tsv', 'LIN7A.tsv', 'LIN7B.tsv', 'SDC2.tsv',
                          'CASKIN1.tsv', 'PPFIA2.tsv', 'EPS8.tsv', 'CFL1.tsv', 'WASL.tsv', 'CFL2.tsv',
                          'PXN.tsv', 'TJP1.tsv', 'GSN.tsv', 'DNM2.tsv', 'WAS.tsv', 'HDAC6.tsv', 'EGF.tsv', 'HBEGF.tsv',
                          'EREG.tsv', 'NRG1.tsv', 'GRB2.tsv', 'ERBB2.tsv', 'ERBB3.tsv', 'NRG2.tsv', 'NRG3.tsv',
                          'NRG4.tsv', 'CACNG8.tsv', 'CNIH2.tsv', 'CAMK2A.tsv', 'EPB41L1.tsv', 'PICK1.tsv', 'GRIK1.tsv',
                          'GRIK5.tsv', 'GRIK3.tsv', 'GRIK4.tsv', 'CALM3.tsv', 'CALML4.tsv', 'CALML3.tsv', 'GRIN2D.tsv',
                          'GRIN2C.tsv', 'GRIN3A.tsv', 'GRIN3B.tsv', 'FYN.tsv', 'GNAQ.tsv', 'ADORA2A.tsv', 'PRNP.tsv',
                          'KCNA1.tsv', 'KCNAB2.tsv', 'KCNAB1.tsv', 'KCNA2.tsv', 'KCNAB3.tsv', 'LLGL2.tsv', 'PRKCI.tsv',
                          'PRKCZ.tsv', 'DUSP1.tsv', 'HSPB2.tsv', 'JUN.tsv', 'MAP2K3.tsv', 'MAP2K6.tsv', 'MAPKAPK5.tsv',
                          'MAPKAPK3.tsv', 'PTPN3.tsv', 'MAPKAPK2.tsv', 'NRXN2.tsv', 'NRXN3.tsv', 'GPHN.tsv',
                          'MDGA1.tsv', 'CBLN1.tsv', 'DAG1.tsv', 'LRRTM2.tsv', 'NXPH1.tsv', 'AKT1.tsv',
                          'PIK3CA.tsv', 'TP53.tsv', 'PIK3R1.tsv', 'MAGI2.tsv', 'MAST2.tsv', 'PTK2.tsv', 'PREX2.tsv',
                          'SPOP.tsv', 'CTNNB1.tsv', 'PSMD4.tsv', 'RAD23A.tsv', 'TSC2.tsv', 'UBE2D1.tsv', 'UBE2D2.tsv',
                          'UBE2L3.tsv']

# , 'EPB41L1.tsv'
files_to_move_to4layer = ['MTOR.tsv', 'HSP90AA1.tsv', 'MDM2.tsv', 'RICTOR.tsv', 'EP300.tsv', 'APP.tsv', 'PPFIA1.tsv',
                          'ILK.tsv', 'ARHGEF9.tsv', 'UBC.tsv', 'STUB1.tsv', 'CACNA2D1.tsv', 'CACNA2D4.tsv',
                          'CACNA1C.tsv', 'CACNA1S.tsv', 'CACNA1D.tsv', 'CACNA2D2.tsv', 'CAMK2B.tsv', 'MAPT.tsv',
                          'CRK.tsv', 'EGFR.tsv', 'LCP2.tsv', 'CRKL.tsv', 'GRID2.tsv', 'PARD6A.tsv', 'PARD3.tsv',
                          'PARD6B.tsv', 'LIMK1.tsv', 'ACTB.tsv', 'ACTA1.tsv', 'ACTG1.tsv', 'YWHAZ.tsv', 'CDH2.tsv',
                          'CAV1.tsv', 'MAPK14.tsv', 'MAPK8.tsv', 'FOS.tsv', 'MAPK11.tsv', 'SHC1.tsv', 'CDH1.tsv',
                          'ABI1.tsv', 'ADAM17.tsv', 'KRAS.tsv', 'HRAS.tsv', 'NPHS1.tsv', 'ADRBK1.tsv', 'NCK2.tsv',
                          'NCK1.tsv', 'IRS2.tsv', 'GRIP1.tsv', 'GRIP2.tsv', 'PRKCA.tsv', 'CACNG4.tsv', 'CASP3.tsv',
                          'KCNA5.tsv', 'MPP5.tsv', 'MPP6.tsv', 'MPP2.tsv', 'PARD6G.tsv', 'MAP3K5.tsv', 'TAOK2.tsv',
                          'MAP3K4.tsv', 'MAPK13.tsv', 'HSPB1.tsv', 'RAC1.tsv', 'IRS1.tsv', 'SQSTM1.tsv', 'UBQLN1.tsv',
                          'BCAR1.tsv', 'ITGB3.tsv', 'VCL.tsv', 'RBX1.tsv', 'AR.tsv', 'GJA1.tsv', 'UBA1.tsv',
                          'ANAPC11.tsv', 'ACTR2.tsv', 'WIPF1.tsv']

files_to_move_to5layer = ['ABL1.tsv', 'ADRB2.tsv', 'ARRB2.tsv', 'UBE2S.tsv', 'APOE.tsv', 'NCOA1.tsv', 'DOCK1.tsv',
                          'ZYX.tsv', 'CACNB2.tsv', 'CACNB3.tsv', 'AKAP5.tsv', 'CALM1.tsv', 'CYCS.tsv', 'TGFBR1.tsv',
                          'CTNND1.tsv', 'JUP.tsv', 'RAPGEF1.tsv', 'NEDD9.tsv', 'STAT3.tsv', 'MEF2A.tsv', 'BRAF.tsv',
                          'RALGDS.tsv', 'HSPA4.tsv', 'HSPA8.tsv', 'LIMS1.tsv', 'IGF1R.tsv', 'INSR.tsv', 'TLN1.tsv',
                          'KDR.tsv', 'VAV1.tsv', 'RHOA.tsv', 'MAP2K4.tsv', 'DEPTOR.tsv', 'MLST8.tsv', 'TIAM1.tsv',
                          'UBE2D3.tsv', 'GABARAPL2.tsv', 'GABARAP.tsv', 'UBE2N.tsv']

original_list = ['NRAS', 'CDH5', 'AKT1S1', 'PRR5', 'MAPKAP1', 'TTI1', 'ATG4B', 'ATG3', 'ATG7', 'ATG4A', 'BECN1', 'ATG5',
                 'ATG12', 'DNAJB1', 'BAG3', 'BAG1', 'BAG2', 'INS', 'PTPN11', 'RAP1A', 'LRPAP1', 'ACTN1', 'UBE2V2',
                 'UBE2V1']
files_to_move_to6layer = [item + '.tsv' for item in original_list]


def move_files_with_extension(source_dir, destination_dir, extension, files_to_move):
    # Get a list of files in the source directory with the specified extension
    # files_to_move = [file for file in os.listdir(source_dir) if file.endswith(extension)]

    # Ensure the destination directory exists; create it if not
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Move each file to the destination directory
    for file_name in files_to_move:
        source_path = os.path.join(source_dir, file_name)
        destination_path = os.path.join(destination_dir, file_name)
        shutil.move(source_path, destination_path)
        print(f"Moved: {file_name}")


# Example usage:
file_extension = '.tsv'  # Replace with the desired file extension
source_directory = 'C:\\Users\\User\PycharmProjects\pythonProject5'  # Replace with the actual source directory path

destination_directory_2layer = 'C:\\Users\\User\PycharmProjects\pythonProject5\\2nd_layer_Proteins_and_their_interactions'  # Replace with the actual destination directory path
move_files_with_extension(source_directory, destination_directory_2layer, file_extension, files_to_move_to2layer)

'''destination_directory_3layer = 'C:\\Users\\User\PycharmProjects\pythonProject5\\3rd_layer_Proteins_and_their_interactions'  # Replace with the actual destination directory path
destination_directory_4layer = 'C:\\Users\\User\PycharmProjects\pythonProject5\\4th_layer_Proteins_and_their_interactions'  # Replace with the actual destination directory path
destination_directory_5layer = 'C:\\Users\\User\PycharmProjects\pythonProject5\\5th_layer_Proteins_and_their_interactions'  # Replace with the actual destination directory path
destination_directory_6layer = 'C:\\Users\\User\PycharmProjects\pythonProject5\\6th_layer_Proteins_and_their_interactions'  # Replace with the actual destination directory path



move_files_with_extension(source_directory, destination_directory_3layer, file_extension, files_to_move_to3layer)
move_files_with_extension(source_directory, destination_directory_4layer, file_extension, files_to_move_to4layer)
move_files_with_extension(source_directory, destination_directory_5layer, file_extension, files_to_move_to5layer)
move_files_with_extension(source_directory, destination_directory_6layer, file_extension, files_to_move_to6layer)
'''
