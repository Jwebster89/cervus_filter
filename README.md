# cervus_filter
## Introduction
cervus_filter filters cervus output results of parentage analysis to produce a list of positions of mismatches between Offspring and Parent. These positions are then checked for coverage and quality and values reported.

## Quick Usage
Cervus can be run as follows

`./cervus_filter -g genotype_file -c cervus_output -s output_from_IonTorrent`

and requires the following files:

### Genotype file
The genotype file can be created with [cervus_parse](https://github.com/bogemad/cervus_parse) and is also the input file used for Cervus.

### cervus_output
The Cervus output file is that produced by the software Cervus for the analysis of parentage.

### output_from_IonTorrent
The Ion Torrent will produce an XLS file from an ampliseq run to be used here.

## Output

cervus_filter will output first a list of Parent and Offspring pairs that have a positive LOD score and 3 or less mismatches according to cervus.

Next, cervus filter will report which Parent/Offspring pair do or don't have mismatches, where those mismatches occur and the coverage and quality of those mismatch positions. E.g.

```
[Offspring] Animal-49762-0005 == Animal-14675-0001 [Parent]
Mismatch in target 848454 for samplesAnimal-49762-0005 and Animal-14675-0001
Coverage = 1356 and Quality = 344.221 for target 848454 in sample Animal-49762-0005
Coverage = 762 and Quality = 7534.77 for target 848454 in sample Animal-14675-0001

[Offspring] Animal-97685-0003 == Animal-78346-0001 [Parent]
There were no mismatches in samples Animal-97685-0003 and Animal-78346-0001
```

## Options and usage
```
usage: cervus_filter.v0.1.3.py -c CSV -g GENOTYPE -s ION_TORRENT [-h]

Cervus_filter

Optional Arguments:
  -h, --help            show this help message and exit

Required Arguments:
  -c CSV, --csv CSV     Output of Cervus in csv format
  -g GENOTYPE, --genotype GENOTYPE
                        input of Cervus (output of Cervus_parse) in csv format
  -s ION_TORRENT, --ion_torrent ION_TORRENT
                        Output of Ion Torrent in tsv format
```
