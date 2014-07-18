#!/usr/bin/perl


use strict;
use warnings;
use CGI;
use Carp;
use CGI::Carp qw(carpout);
use Switch;

require "./cgiHelper.pl";

my $UPLOAD = "../uploads/";
my $RESULT = "../results/";
my $safe_chars = "A-Za-z0-9_.-";

$ENV{'GENOME_DB'} = "/Volumes/AltLab/Genomes";

# Flush output after every write
select( (select(STDOUT), $| = 1 )[0] );



my $q = CGI->new;
print $q->header;
print $q->start_html("TLX Hot Spots");
print $q->p("Processing Request...");
my $tlxfile = cgiUpload($q,'tlxfile',$UPLOAD);

unless ($tlxfile =~ /\.tlx$/) {
  unlink $tlxfile;
  croak "Error: file must contain .tlx suffix";
}

my $assembly = $q->param('assembly');
my $binwidth = $q->param('binwidth');
my $bgwidth = $q->param('bgwidth');
my $alpha_exp = $q->param('alpha');
my $alpha = 10**(-$alpha_exp);
my $hitsmin = $q->param('hitsmin');
my $strandmin = $q->param('strandmin');



my ($path,$name,$ext) = parseFilename($tlxfile);
my $output = "$RESULT/$name";




my $cmd = join(" ","Rscript /Users/robin/TranslocPipeline/R/TranslocHotSpots.R",
                        "$tlxfile $output",
                        "bin.width=$binwidth",
                        "bg.width=$bgwidth",
                        "alpha=$alpha",
                        "hits.min=$hitsmin",
                        "strand.min=$strandmin",
                        "cores=4");
                        
System($cmd) or croak "Error: $cmd";

print $q->p("Finished processing request.");
print $q->a({href=>"../results/"},"Download your results here.");

$q->end_html();

unlink $tlxfile;



BEGIN {
    carpout("STDOUT");
}


