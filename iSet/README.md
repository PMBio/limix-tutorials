# Interaction set test (iSet)

Set tests are a powerful approach for association testing between groups of genetic variants and quantitative traits.
In this tutorial we showcase the usage of iSet, efficient set tests for gene-context interactions.
iSet is part of the mixed-model software suite LIMIX (https://github.com/PMBio/limix).

As we show in this tutorial, iSet can be applied for interaction analysis in two data designs:
* complete design, where all individuals have been phenotyped in each context
* stratified design, where each individual has been phenotyped in only one of the two contexts

Below we showcase the usage of iSet using a command line interface (using the limix scripts `mtSet_preprocess`, `iSet_analyze` and `iSet_postprocess`).

iSet can be also used in Python as we describe in this [iPython notebook](https://github.com/PMBio/limix-tutorials/blob/master/iSet/Interaction_set_test.ipynb).

By Francesco Paolo Casale (casale@ebi.ac.uk), Danilo Horta (horta@ebi.ac.uk) and Oliver Stegle (stegle@ebi.ac.uk)

## Quick Start

* Download and install Limix
```bash
git clone --depth 1 https://github.com/PMBio/limix.git
pushd limix
python setup.py install
```
* Download sample data from http://www.ebi.ac.uk/~casale/data.zip and unzip them
```bash
wget http://www.ebi.ac.uk/~casale/data.zip
unzip data.zip
```
* Define sets to consider in the analysis and export to file WFILE (see below for further information)
```bash
BFILE=data/chrom22_subsample20_maf0.10 #bed file basename
WFILE=data/windows #file with the sets to analyse
mtSet_preprocess --precompute_windows --bfile $BFILE --wfile $WFILE --window_size 30000 --plot_windows
```
* Perform set tests from window 0 to window 9 for either complete or stratified designs (see below for further information). This command can be used to run iSet on multiple cores, each analysing a set of windows (for example, 0-9, 10-19, 20-29, etc).
    - Complete design
    ```bash
    PFILE=data/pheno_compl #phenotype matrix (N samples x 2)
    FFILE=data/covs #covariates (N samples x N covariates)
    RESDIR=results #output folder
    iSet_analyze --bfile $BFILE --ffile $FFILE --pfile $PFILE --wfile $WFILE --minSnps 4 --resdir $RESDIR --start_wnd 0 --end_wnd 10
    ```
    - Stratified design
    ```bash
    PFILE=data/pheno_strat #phenotype vector (N samples x 1)
    FFILE=data/covs #covariates (N samples x N covariates)
    IFILE=data/indicator #environment indicator vector (0/1, N samples x 1)
    RESDIR=results #output folder
    iSet_analyze --bfile $BFILE --ffile $FFILE --pfile $PFILE --wfile $WFILE --minSnps 4 --resdir $RESDIR --start_wnd 0 --end_wnd 10 --ifile $IFILE
    ```
* Merges all results present in RESDIR, calculate P values and exports to OUTFILE
```bash
OUTFILE=final
iSet_postprocess --resdir $RESDIR --outfile $OUTFILE
```

## Precomputing the windows
In order to apply iSet, the user is required to provide a file (wfile) that contains the variant-sets to consider in the analysis. The file needs to have the following format:
* the rows correspond to the different variant sets,
* the columns indicate: index, chromosome, start position, end position, index of startposition (in the bed file) and number of SNPs (6 columns).

While the user can specify the sets to consider arbitrarily, we here provide a method that produce the set file for sliding-window experiments:


```bash
mtSet_preprocess --precompute_windows --bfile bfile --wfile wfile --window_size window_size --plot_windows
```

where
* __bfile__ is the base name of of the binary bed file (__bfile__.bim is required).
* __window\_size__ is the size of the window (in basepairs). The default value is 30kb.
* __wfile__ is the base name of the output file.
  If not specified, the file is saved as __bfile__.window\_size.wnd in the current folder (output format described above).
* __plot\_windows__ if the flag is set, a histogram over the number of markers within a window is generated and saved as __wfile__.pdf.

## Running analysis

The set test can be run by the following analysis script:

```bash
iSet_analyze --bfile bfile --pfile pfile --wfile wfile --ffile ffile --minSnps minSnps --start_wnd start_wnd --end_wnd end_wnd --resdir rdir --ifile $IFILE --n_perms 10
```

where

- __bfile__ is the base name of of the binary bed file (__bfile__.bed, __bfile__.bim, __bfile__.fam are required).
- __pfile__ is the base name of the phenotype file. The script requires the file __pfile__.phe containing the phenotype data.
- __wfile__ is the base name of the file containing the windows to be considered in the set test. The script requires the file __wfile__.wnd.
- __ffile__ is the name of the file containing the covariates. Each covariate is a column in the matrix.
- __start\_wnd__ is the index of the start window
- __end\_wnd__ is the index of the end window
- __minSnps__ if set only windows containing at least minSnps are considered in the analysis
rdir is the directory to which the results are exported.
- __n_perms__ number of null (sampled) test statistics (obtained thrugh permutations/parametric bootstraps)
- __rdir__ is the directory to which the results are exported. The command exports files *start_wnd*_*end_wnd*.iSet.real that contains test statistics and vairance components and *start_wnd*_*end_wnd*.iSet.perm that contains null statistics
- __ifile__ is the file path to a csv file containing an indicator (True or False) for each sample. If specified the analysis is performed for a stratified design.
- __startwnd\_endwnd__.res and contains results in the following format: window index, chromosome, start position, stop position, index of startposition, number of SNPs and log likelihood ratio.

Note that this command can be used to run iSet on multiple cores, each analysing a set of windows (for example, 0-9, 10-19, 20-29, etc).

## Postprocessing

After running iSet, the following script can be used to merge the result files and estimate the p-values (p-values are obtained by a parametric fit of the test statistics): 

```bash
iSet_postprocess --resdir resdir --outfile outfile --strat
```

where 
* __resdir__ is a pointer to the folder containing the result files of the analysis.
* __outfile__ is the prefix of the two output files.
__outfile__.perm lists the test statistics (first column) and p-values (second column) of the permutated windows
__outfile__.test contains the (index, chromosome, start position, stop position, SNP index, number of SNPs, test statistics and p-value) of each window. Each window is saved in one row.
* __strat__ is a boolean flag that indicates stratified design when used.


