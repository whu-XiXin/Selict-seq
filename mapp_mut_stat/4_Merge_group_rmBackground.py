import os
import pandas as pd
import argparse

def main(input_file, bg_dir, output_file):
    # Read all first two columns from a set of files and remove duplicates
    df_dedup = pd.DataFrame()
    for dedup_filename in os.listdir(bg_dir):
        if dedup_filename.endswith('.txt'):
            filepath = os.path.join(bg_dir, dedup_filename)
            df_temp = pd.read_csv(filepath, header=None, sep='\t', usecols=[0, 1])
            df_dedup = pd.concat([df_dedup, df_temp], ignore_index=True)

    unique_rows_in_dedup_files = df_dedup.drop_duplicates()

    # Read the input file
    df_target = pd.read_csv(input_file, header=None, sep='\t')

    # Ensure DataFrame has at least three columns
    if len(df_target.columns) < 3:
        print(f"{input_file} file does not have enough columns")
        return

    # Remove rows from the target file that match the first two columns in the deduplication files
    target_tuples = df_target.iloc[:, :2].apply(tuple, axis=1)
    dedup_tuples = unique_rows_in_dedup_files.apply(tuple, axis=1)
    filtered_df = df_target[~target_tuples.isin(dedup_tuples)]

    # Output to a new file
    filtered_df.to_csv(output_file, sep='\t', index=False, header=False)
    print(f"The processed results have been saved to {output_file}")

    # Prepare BED format output: first column, second column value minus 1, third column
    bed_output_file = f"{os.path.splitext(output_file)[0]}.bed"
    bed_df = filtered_df.copy()
    bed_df[1] = bed_df[1] - 1  # Adjust the second column by subtracting 1
    bed_df.iloc[:, :3].to_csv(bed_output_file, sep='\t', index=False, header=False)
    print(f"The BED formatted results have been saved to {bed_output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This script removes rows from an input file based on duplicates found in a set of background files and outputs a BED-formatted file.")
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-bg', '--background_directory', required=True, help='Directory containing background files for deduplication')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    args = parser.parse_args()

    main(args.input, args.background_directory, args.output)