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
print $q->start_html("SHMPlot");
print $q->p("Processing Request...");

my $datafile = cgiUpload($q,'datafile',$UPLOAD);

unless ($datafile =~ /\.txt$/) {
  unlink $datafile;
  croak "Error: file must be saved in Tab-Delimited Text format and contain .txt suffix";
}

my $tstart = $q->param('tstart');
my $tend = $q->param('tend');
my $ymax = $q->param('ymax');
my $plotrows = $q->param('plotrows');
my $figureheight = $q->param('figureheight');
my $showsequence = defined $q->param('showsequence') ? "T" : "F";



my ($path,$name,$ext) = parseFilename($datafile);

my $shmplot_cmd = join(" ",
                        "Rscript",
                        "/Users/robin/SHMSanger/R/SHMPlot.R",
                        $datafile,
                        "$RESULT/$name.pdf",
                        "tstart=$tstart",
                        "tend=$tend",
                        "ymax=$ymax",
                        "plotrows=$plotrows",
                        "figureheight=$figureheight",
                        "showsequence=$showsequence");
System($shmplot_cmd) or croak "Error: $shmplot_cmd";

print $q->p("Finished processing request.");
print $q->a({href=>"../results/"},"Download your results here.");

$q->end_html();

unlink $datafile;



BEGIN {
    carpout("STDOUT");
}


