import pandas as pd
import argparse

def main(file1, file2, output):
    # Read data
    df_a = pd.read_csv(file1, header=None, sep='\t')
    df_b = pd.read_csv(file2, header=None, sep='\t')

    # Check number of columns in each DataFrame
    print(f"df_a columns: {len(df_a.columns)}")
    print(f"df_b columns: {len(df_b.columns)}")

    # Merge data
    merged_df = pd.merge(df_a, df_b, left_on=[df_a.columns[0], df_a.columns[1]], right_on=[df_b.columns[0], df_b.columns[1]], how='inner')

    # Filtering condition: Adjust according to actual column names after merging
    filtered_df = merged_df[
        ((merged_df['2_x'] + ' ' + merged_df['3_x'] + ' ' + merged_df['4_x']) == 'A G reverse') |
        ((merged_df['2_x'] + ' ' + merged_df['3_x'] + ' ' + merged_df['4_x']) == 'T C forward') |
        ((merged_df['2_y'] + ' ' + merged_df['3_y'] + ' ' + merged_df['4_y']) == 'A G reverse') |
        ((merged_df['2_y'] + ' ' + merged_df['3_y'] + ' ' + merged_df['4_y']) == 'T C forward')
    ]

    # Save the result as a txt file with tab delimiter, without index
    filtered_df.to_csv(output, sep='\t', index=False, header=False)
    print(f"Filtered results have been saved to {output}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This script merges parallel group and filters based of AtoG reverse and TtoC forward.")
    parser.add_argument('-1', '--input1', required=True, help='Input file for group 1')
    parser.add_argument('-2', '--input2', required=True, help='Input file for group 2')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    args = parser.parse_args()

    main(args.input1, args.input2, args.output)