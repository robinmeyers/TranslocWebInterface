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
print $q->start_html("SHMViz");
print $q->p("Processing Request...");

my $output = $q->param('output');
$output =~ s/[^$safe_chars]/_/g;
croak "Error: please name your file" unless $output =~ /\S/;

my $clonefile = cgiUpload($q,'clonefile',$UPLOAD);

unless ($clonefile =~ /\.txt$/) {
  unlink $clonefile;
  croak "Error: file must be saved in Tab-Delimited Text format and contain .txt suffix";
}

my $mutfile = cgiUpload($q,'mutfile',$UPLOAD);

unless ($mutfile =~ /\.txt$/) {
  unlink $mutfile;
  croak "Error: file must be saved in Tab-Delimited Text format and contain .txt suffix";
}

my $refseqfile = cgiUpload($q,'refseqfile',$UPLOAD);

unless ($refseqfile =~ /\.(fa|fas)$/) {
  unlink $refseqfile;
  croak "Error: file must be in fasta format and contain .fa or .fas suffix";
}

my $tstart = $q->param('tstart');
my $tend = $q->param('tend');
my $plotrows = $q->param('plotrows');
my $blankclones = defined $q->param('blankclones') ? "T" : "F";
my $showsubs = defined $q->param('showsubs') ? "T" : "F";
my $showdels = defined $q->param('showdels') ? "T" : "F";
my $showins = defined $q->param('showin') ? "T" : "F";
my $showsequence = defined $q->param('showsequence') ? "T" : "F";
my $figureheight = $q->param('figureheight');
my $regex1 = $q->param('regex1');
my $regex2 = $q->param('regex2');


my $shmviz_cmd = join(" ","Rscript",
                              "/Users/robin/SHMPipeline/R/SHMViz.R",
                              "$mutfile $clonefile $refseqfile $RESULT/${output}_viz.pdf",
                              "tstart=$tstart tend=$tend",
                              "plotrows=$plotrows blankclones=$blankclones",
                              "showsubs=$showsubs showdels=$showdels",
                              "showins=$showins showsequence=$showsequence",
                              "figureheight=$figureheight",
                              "regex1=$regex1 regex2=$regex2");

System($shmviz_cmd) or croak "Error: $shmviz_cmd";

print $q->p("Finished processing request.");
print $q->a({href=>"../results/"},"Download your results here.");

$q->end_html();

unlink $clonefile;
unlink $mutfile;
unlink $refseqfile;



BEGIN {
    carpout("STDOUT");
}


