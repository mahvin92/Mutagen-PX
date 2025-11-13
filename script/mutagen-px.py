import pandas as pd
from pathlib import Path
import argparse

def read_fasta(filename):
    """Reads a single-sequence FASTA file into a string."""
    seq = []
    with open(filename) as f:
        for line in f:
            if not line.startswith(">"):
                seq.append(line.strip())
    return "".join(seq)

def write_fasta(sequences, filename):
    """Writes patient sequences into a FASTA file."""
    with open(filename, "w") as f:
        for sample, seq in sequences.items():
            f.write(f">{sample}\n")
            for i in range(0, len(seq), 80):
                f.write(seq[i:i+80] + "\n")

def apply_mutations(ref_seq, mutations):
    """Apply mutations (list of dicts) to the reference sequence."""
    seq = list(ref_seq)
    
    # Sort mutations by start position descending (important for insertions/deletions)
    mutations = sorted(
        mutations, 
        key=lambda x: int(x['start']) if str(x['start']).isdigit() else 0, 
        reverse=True
    )

    for mut in mutations:
        start = mut['start']
        end = mut['end']
        ref = mut['reference']
        alt = mut['change']

        # Skip wildtype
        if str(start).lower() == "no variant":
            continue

        start = int(start) - 1  # convert to 0-based index
        end = int(end)          # python slice is exclusive

        if ref == "-" and alt != "-":
            # insertion
            seq[start:start] = list(alt)
        elif alt == "-" and ref != "-":
            # deletion
            del seq[start:end]
        else:
            # substitution
            seq[start:end] = list(alt)

    return "".join(seq)

def main():
    parser = argparse.ArgumentParser(description="Generate mutated gene profiles from patient mutation data.")
    parser.add_argument("--gene", required=True, help="Gene symbol or name (used for file naming).")
    parser.add_argument("--ref", required=True, help="Path to reference sequence (FASTA).")
    parser.add_argument("--profile", required=True, help="Path to mutation profile (TSV).")
    parser.add_argument("--outdir", default="output", help="Directory to save output FASTA.")
    args = parser.parse_args()

    gene_name = args.gene
    ref_path = Path(args.ref)
    profile_path = Path(args.profile)
    out_path = Path(args.outdir)
    out_path.mkdir(exist_ok=True)

    # Load reference sequence
    ref_seq = read_fasta(ref_path)

    # Load mutation profile
    df = pd.read_csv(profile_path, sep="\t")

    patient_sequences = {}

    # Group by patient sample
    for sample, group in df.groupby("sample"):
        mutations = group.rename(columns={
            f"{gene_name} start": "start",
            f"{gene_name} end": "end",
            "reference": "reference",
            "change": "change"
        }).to_dict("records")

        # Check for wildtype
        if all(str(m['start']).lower() == "no variant" for m in mutations):
            patient_sequences[sample] = ref_seq
        else:
            patient_sequences[sample] = apply_mutations(ref_seq, mutations)

    # Write output
    output_file = out_path / f"{gene_name}-patients.fasta"
    write_fasta(patient_sequences, output_file)
    print(f"✅ Generated mutated sequences: {output_file}")

if __name__ == "__main__":
    main()
