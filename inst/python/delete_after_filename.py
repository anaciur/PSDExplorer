import os

files_to_move_to3layer =  ['ARHGEF6.tsv', 'CDC42.tsv', 'PAK2.tsv', 'PAK3.tsv', 'PAK1.tsv', 'GIT2.tsv', 'GIT1.tsv', 'CBL.tsv', 'SCRIB.tsv', 'SRC.tsv', 'CACNB4.tsv', 'CACNG1.tsv', 'GRIA4.tsv', 'GRIA2.tsv', 'SHISA9.tsv', 'GRIA3.tsv', 'APBA1.tsv', 'LIN7C.tsv', 'LIN7A.tsv', 'LIN7B.tsv', 'SDC2.tsv', 'CASKIN1.tsv', 'WHRN.tsv', 'PPFIA2.tsv', 'EPS8.tsv', 'CFL1.tsv', 'WASL.tsv', 'CFL2.tsv', 'PXN.tsv', 'TJP1.tsv', 'GSN.tsv', 'DNM2.tsv', 'WAS.tsv', 'HDAC6.tsv', 'EGF.tsv', 'HBEGF.tsv', 'EREG.tsv', 'NRG1.tsv', 'GRB2.tsv', 'ERBB2.tsv', 'ERBB3.tsv', 'NRG2.tsv', 'NRG3.tsv', 'NRG4.tsv', 'CACNG8.tsv', 'CNIH2.tsv', 'CAMK2A.tsv', 'EPB41L1.tsv', 'PICK1.tsv', 'GRIK1.tsv', 'GRIK5.tsv', 'GRIK3.tsv', 'GRIK4.tsv', 'CALM3.tsv', 'CALML4.tsv', 'CALML3.tsv', 'GRIN2D.tsv', 'GRIN2C.tsv', 'GRIN3A.tsv', 'GRIN3B.tsv', 'FYN.tsv', 'GNAQ.tsv', 'ADORA2A.tsv', 'PRNP.tsv', 'KCNA1.tsv', 'KCNAB2.tsv', 'KCNAB1.tsv', 'KCNA2.tsv', 'KCNAB3.tsv', 'LLGL2.tsv', 'PRKCI.tsv', 'PRKCZ.tsv', 'DUSP1.tsv', 'HSPB2.tsv', 'JUN.tsv', 'MAP2K3.tsv', 'MAP2K6.tsv', 'MAPKAPK5.tsv', 'MAPKAPK3.tsv', 'PTPN3.tsv', 'MAPKAPK2.tsv', 'NRXN2.tsv', 'NRXN3.tsv', 'GPHN.tsv', 'MDGA1.tsv', 'CBLN1.tsv', 'DAG1.tsv', 'NLGN4Y.tsv', 'LRRTM2.tsv', 'NXPH1.tsv', 'AKT1.tsv', 'PIK3CA.tsv', 'TP53.tsv', 'PIK3R1.tsv', 'MAGI2.tsv', 'MAST2.tsv', 'PTK2.tsv', 'PREX2.tsv', 'SPOP.tsv', 'CTNNB1.tsv', 'PSMD4.tsv', 'RAD23A.tsv', 'TSC2.tsv', 'UBE2D1.tsv', 'UBE2D2.tsv', 'UBE2L3.tsv']

# , 'EPB41L1.tsv'
files_to_move_to4layer = ['MTOR.tsv', 'HSP90AA1.tsv', 'MDM2.tsv', 'RICTOR.tsv', 'EP300.tsv', 'APP.tsv', 'PPFIA1.tsv', 'ILK.tsv', 'ARHGEF9.tsv', 'UBC.tsv', 'STUB1.tsv', 'CACNA2D1.tsv', 'CACNA2D4.tsv', 'CACNA1C.tsv', 'CACNA1S.tsv', 'CACNA1D.tsv', 'CACNA2D2.tsv', 'CAMK2B.tsv', 'MAPT.tsv', 'CRK.tsv', 'EGFR.tsv', 'LCP2.tsv', 'CRKL.tsv', 'GRID2.tsv', 'PARD6A.tsv', 'PARD3.tsv', 'PARD6B.tsv', 'LIMK1.tsv', 'ACTB.tsv', 'ACTA1.tsv', 'ACTG1.tsv', 'YWHAZ.tsv', 'CDH2.tsv', 'CAV1.tsv', 'MAPK14.tsv', 'MAPK8.tsv', 'FOS.tsv', 'MAPK11.tsv', 'SHC1.tsv', 'CDH1.tsv', 'ABI1.tsv', 'ADAM17.tsv', 'KRAS.tsv', 'HRAS.tsv', 'NPHS1.tsv', 'ADRBK1.tsv', 'NCK2.tsv', 'NCK1.tsv', 'IRS2.tsv', 'GRIP1.tsv', 'GRIP2.tsv', 'PRKCA.tsv', 'CACNG4.tsv', 'CASP3.tsv', 'KCNA5.tsv', 'MPP5.tsv', 'MPP6.tsv', 'MPP2.tsv', 'PARD6G.tsv', 'MAP3K5.tsv', 'TAOK2.tsv', 'MAP3K4.tsv', 'MAPK13.tsv', 'HSPB1.tsv', 'RAC1.tsv', 'IRS1.tsv', 'SQSTM1.tsv', 'UBQLN1.tsv', 'BCAR1.tsv', 'ITGB3.tsv', 'VCL.tsv', 'RBX1.tsv', 'AR.tsv', 'GJA1.tsv', 'UBA1.tsv', 'ANAPC11.tsv', 'ACTR2.tsv', 'WIPF1.tsv']

original_list_5layer = ['ABL1', 'ADRB2', 'ARRB2', 'UBE2S', 'APOE', 'NCOA1', 'DOCK1', 'ZYX', 'CACNB2', 'CACNB3', 'AKAP5', 'CALM1', 'CYCS', 'TGFBR1', 'CTNND1', 'JUP', 'RAPGEF1', 'NEDD9', 'STAT3', 'MEF2A', 'BRAF', 'RALGDS', 'HSPA4', 'HSPA8', 'LIMS1', 'IGF1R', 'INSR', 'TLN1', 'KDR', 'VAV1', 'RHOA', 'MAP2K4', 'DEPTOR', 'MLST8', 'TIAM1', 'UBE2D3', 'GABARAPL2', 'GABARAP', 'UBE2N']
files_to_move_to5layer = [item + '.tsv' for item in original_list_5layer]

original_list_6layer = ['NRAS','CDH5','AKT1S1','PRR5','MAPKAP1','TTI1','ATG4B','ATG3','ATG7','ATG4A','BECN1','ATG5','ATG12','DNAJB1','BAG3','BAG1','BAG2','INS','PTPN11','RAP1A','LRPAP1','ACTN1','UBE2V2','UBE2V1']
files_to_move_to6layer = [item + '.tsv' for item in original_list_6layer]


def delete_after_name(file_list):
    try:
        for file_path in file_list:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        print("All files in the directory have been deleted.")
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")

    except Exception as e:
        print(f"An error occurred: {e}")


delete_after_name(files_to_move_to3layer)
delete_after_name(files_to_move_to4layer)
delete_after_name(files_to_move_to5layer)
delete_after_name(files_to_move_to6layer)