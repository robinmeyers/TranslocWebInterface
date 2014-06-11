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


# Flush output after every write
select( (select(STDOUT), $| = 1 )[0] );


my $q = CGI->new;
print $q->header;
print $q->start_html("SHMProfile");
print $q->p("Processing Request...");



my $tlxfile = cgiUpload($q,'tlxfile',$UPLOAD);

unless ($tlxfile =~ /\.tlx$/) {
  unlink $tlxfile;
  croak "Error: file must be saved in Tab-Delimited Text format and contain .tlx suffix";
}

my $output = $RESULT . basename($tlxfile,".tlx") . "_switch.pdf";

my $numbins = $q->param('numbins');
my $facetscales = $q->param('facetscales');


my $switchplot_cmd = join(" ","Rscript",
                              "/Users/robin/TranslocPipeline/R/plotSwitchRegions.R",
                              "$tlxfile $output",
                              "facetscales=$facetscales numbins=$numbins");
System($switchplot_cmd) or croak "Error: $switchplot_cmd";

print $q->p("Finished processing request.");
print $q->a({href=>"../results/"},"Download your results here.");

$q->end_html();

unlink $tlxfile;


BEGIN {
    carpout("STDOUT");
}


