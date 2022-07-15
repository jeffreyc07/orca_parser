import sys
import re
import csv
import argparse

def main(argv):
    parser = argparse.ArgumentParser("orca_parser")
    parser.add_argument("filename", type=str, help='.out filename')
    parser.add_argument("--runtype","-rt",type=str, default="OPT",help="Outfile runtype, either OPT or SOC")
    args = parser.parse_args(argv)

    filename = args.filename.strip()
    runtype = args.runtype

    if runtype == "SOC":
        with open(str(filename + ".out"),"r") as infile:
            filelist = infile.readlines()
        transition = []
        runtime = []
        for line in filelist:
            transition_line = re.search("\s{3}(0)\s*?(\d*?)\s*?(\d*\.\d*?)\s*?(\d*?\.\d*?)\s*?(\d*?\.\d*?)\s*?(\d*?\.\d*?)\s*(\d*?\.\d*?)\s*?(\d*?\.\d*?)\s*?(\d*?\.\d*)",line)
            if transition_line:
                transition.append((transition_line[1],transition_line[2],transition_line[3],transition_line[4],transition_line[5],transition_line[6],transition_line[7],transition_line[8],transition_line[9]))

        for line in filelist:
            runtime_line = re.search("(\d*)\s[a-z]{4}\s(\d*)\s[a-z]{5}\s(\d*)\s[a-z]{7}\s(\d*)\s[a-z]{7}\s(\d*)\s[a-z]{4}", line)
            if runtime_line:
                runtime.append((runtime_line[0],runtime_line[1],runtime_line[2],runtime_line[3],runtime_line[4],runtime_line[5]))

        transition_E_len = int(len(transition)*0.5)
        transition_E = transition[0:transition_E_len]

        # Writing the SOC absorbance spectrum results to csv
        energy_filename = str(filename + "_SOC_TDM.csv")
        with open(str(energy_filename),"w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            fieldnames=['initial_state','final_State','energy(cm-1)','wavelength(nm)','fosc','T2','TX','TY','TZ']
            writer.writerow(fieldnames)
            for row in transition_E:
                writer.writerow(row)

        # Writing the runtime results into csv
        runtime_filename = str(filename + "_runtime.csv")
        total_time_seconds = float(runtime[0][1]) * 24 * 60 * 60 + float(runtime[0][2]) * 60 * 60 + float(runtime [0][3]) * 60 + float(runtime[0][4]) + float(runtime[0][5]) * 1e-3
        with open(str(runtime_filename),"w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            runtime_fieldnames=['days','hours','minutes','seconds','miliseconds','total_time_seconds']
            writer.writerow(runtime_fieldnames)
            runtime_row = [runtime[0][1],runtime[0][2],runtime[0][3],runtime[0][4],runtime[0][5],total_time_seconds]
            writer.writerow(runtime_row)
    else:
        with open(str(filename + ".out"),"r") as infile:
            filelist = infile.readlines()
        
        # Writing the energy results to csv
        energy_list = re.findall("Total Energy\s+\:\s+(-?\d+.?\d*)\s+Eh\s+(-?\d+.?\d*)\s+eV","".join(filelist))
        energy_filename = str(filename + "_geom_energy.csv")

        with open(str(energy_filename),"w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            energy_fieldnames=['Energy(Hartree)','Energy(eV)']
            writer.writerow(energy_fieldnames)
            for row in energy_list:
                writer.writerow(row)

        # Writing the runtime results into csv
        runtime = []
        for line in filelist:
            runtime_line = re.search("(\d*)\s[a-z]{4}\s(\d*)\s[a-z]{5}\s(\d*)\s[a-z]{7}\s(\d*)\s[a-z]{7}\s(\d*)\s[a-z]{4}", line)
            if runtime_line:
                runtime.append((runtime_line[0],runtime_line[1],runtime_line[2],runtime_line[3],runtime_line[4],runtime_line[5]))
        
        runtime_filename = str(filename + "_runtime.csv")
        total_time_seconds = float(runtime[0][1]) * 24 * 60 * 60 + float(runtime[0][2]) * 60 * 60 + float(runtime [0][3]) * 60 + float(runtime[0][4]) + float(runtime[0][5]) * 1e-3

        with open(str(runtime_filename),"w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            runtime_fieldnames=['days','hours','minutes','seconds','miliseconds','total_time_seconds']
            writer.writerow(runtime_fieldnames)
            runtime_row = [runtime[0][1],runtime[0][2],runtime[0][3],runtime[0][4],runtime[0][5],total_time_seconds]
            writer.writerow(runtime_row)
    print(filename + " PARSE COMPLETE")

main(sys.argv[1:])