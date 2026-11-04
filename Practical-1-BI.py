# DNA Sequence Analysis
# Finding Motifs, GC Content and Coding Regions

# Given DNA sequence
dna = "ATGCGATCGATCGATGCTAGCTAGCTAACGATGAAATGCGTAGCTAGCTAA"

# Convert sequence to uppercase
dna = dna.upper()

print("DNA SEQUENCE ANALYSIS")
print("-" * 40)

# Display original sequence
print("DNA Sequence:", dna)
print("Sequence Length:", len(dna))


# --------------------------------------------------
# 1. BASIC DNA SEQUENCE MANIPULATION
# --------------------------------------------------

print("\n1. BASIC SEQUENCE MANIPULATION")
print("-" * 40)

# Count individual nucleotides
print("Number of A:", dna.count("A"))
print("Number of T:", dna.count("T"))
print("Number of G:", dna.count("G"))
print("Number of C:", dna.count("C"))

# Complement
complement = dna.translate(str.maketrans("ATGC", "TACG"))

# Reverse
reverse = dna[::-1]

# Reverse Complement
reverse_complement = complement[::-1]

print("Complement:", complement)
print("Reverse:", reverse)
print("Reverse Complement:", reverse_complement)


# --------------------------------------------------
# 2. MOTIF IDENTIFICATION
# --------------------------------------------------

print("\n2. MOTIF IDENTIFICATION")
print("-" * 40)

# Motif to search
motif = "ATG"

print("Motif:", motif)

positions = []

start = 0

while True:
    position = dna.find(motif, start)

    if position == -1:
        break

    positions.append(position + 1)  # Convert to 1-based position
    start = position + 1

if positions:
    print("Motif found at positions:", positions)
    print("Number of occurrences:", len(positions))
else:
    print("Motif not found.")


# --------------------------------------------------
# 3. GC CONTENT CALCULATION
# --------------------------------------------------

print("\n3. GC CONTENT")
print("-" * 40)

g_count = dna.count("G")
c_count = dna.count("C")

gc_content = ((g_count + c_count) / len(dna)) * 100

print("Number of G:", g_count)
print("Number of C:", c_count)
print("GC Content: {:.2f}%".format(gc_content))


# --------------------------------------------------
# 4. IDENTIFICATION OF CODING REGIONS / ORFs
# --------------------------------------------------

print("\n4. CODING REGION IDENTIFICATION")
print("-" * 40)

start_codon = "ATG"
stop_codons = ["TAA", "TAG", "TGA"]

orfs = []

for i in range(len(dna) - 2):

    # Check for start codon
    if dna[i:i+3] == start_codon:

        # Search for a stop codon in the same reading frame
        for j in range(i + 3, len(dna) - 2, 3):

            codon = dna[j:j+3]

            if codon in stop_codons:

                orf = dna[i:j+3]

                orfs.append((i + 1, j + 3, orf))

                break


if orfs:

    print("Potential Coding Regions / ORFs:")

    for number, (start, end, sequence) in enumerate(orfs, 1):

        print("\nORF", number)
        print("Start Position:", start)
        print("End Position:", end)
        print("Length:", len(sequence))
        print("Sequence:", sequence)

else:

    print("No potential coding regions found.")


print("\nAnalysis completed successfully.")
print("Aditya Rade   BEAD23167")