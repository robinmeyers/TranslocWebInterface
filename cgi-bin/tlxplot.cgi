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
print $q->start_html("TLX Plot");
print $q->p("Processing Request...");

my $tlxfile = cgiUpload($q,'tlxfile',$UPLOAD);

unless ($tlxfile =~ /\.tlx$/) {
  unlink $tlxfile;
  croak "Error: file must contain .tlx suffix";
}

my $assembly = $q->param('assembly');
my $brkchr = $q->param('brkchr');
my $brksite = $q->param('brksite');
my $brkstrand = $q->param('brkstrand');

my $strand = $q->param('strand');
my $binsize = $q->param('binsize');

my $chr = $q->param('chr');
my $start = $q->param('start');
my $end = $q->param('end');
my $mid = $q->param('mid');
my $window = $q->param('window');
my $binnum = $q->param('binnum');

my $plottype = $q->param('plottype');
my $plotshape = $q->param('plotshape');

my $ymax = $q->param('ymax');

my $showY = $q->param('showY');
my $showM = $q->param('showM');

my $featurefile = cgiUpload($q,'featurefile',$UPLOAD);

my ($path,$name,$ext) = parseFilename($tlxfile);
my $pdffile = "$RESULT/$name.pdf";
my $binfile = "$RESULT/${name}_bins.txt";

my $syscmd = "/Users/robin/TranslocPipeline/R/TranslocPlot.R $tlxfile $pdffile binfile=$binfile assembly=$assembly strand=$strand";

if ($brkchr && $brksite) {
  $brkchr = lc($brkchr);
  $brkchr = "chr$brkchr" unless $brkchr =~ /^chr/;
  $syscmd .= " brkchr=$brkchr brksite=$brksite";
  $syscmd .= " brkstrand=$brkstrand" if $brkstrand;
}

if ($chr) {
  $chr = lc($chr);
  $chr = "chr$chr" unless $chr =~ /^chr/;

  $syscmd .= " chr=$chr";
  if ($mid && $window) {
    $syscmd .= " rmid=$mid rwindow=$window";
  } elsif ($start && $end) {
    $syscmd .= " rstart=$start rend=$end";
  }

  if ($binnum) {
    $syscmd .= " binnum=$binnum";
  } else {
    $syscmd .= " binnum=100"; 
  }

  $syscmd .= " plottype=$plottype";

  if ($plottype eq "dot") {
    if ($strand == 2) {
      $syscmd .= " plotshape=diamond";
    } else {
      $syscmd .= " plotshape=$plotshape";
    }
  } else {
    $syscmd .= " ymax=$ymax" if $ymax;
  }

  $syscmd .= " featurefile=$featurefile" if $featurefile;


} else {

  $syscmd .= " binsize=$binsize";

  $syscmd .= " plottype=dot";
  if ($strand == 2) {
    $syscmd .= " plotshape=diamond";
  } else {
    $syscmd .= " plotshape=$plotshape";
  }

  $syscmd .= " showY=1" if $showY;
  $syscmd .= " showM=1" if $showM;

}



System("$syscmd") or croak "Error: failed executing the following command:<br>$syscmd<br>";

print $q->p("Finished processing request.");
print $q->a({href=>"../results/"},"Download your results here.");

$q->end_html();

unlink $tlxfile;



BEGIN {
    carpout("STDOUT");
}


