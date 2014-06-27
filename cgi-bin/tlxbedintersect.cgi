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
print $q->start_html("TLX-BED Intersect");
print $q->p("Processing Request...");
my $tlxfile = cgiUpload($q,'tlxfile',$UPLOAD);

unless ($tlxfile =~ /\.tlx$/) {
  unlink $tlxfile;
  croak "Error: file must contain .tlx suffix";
}

my $bedfile = cgiUpload($q,'bedfile',$UPLOAD);
unless ($bedfile =~ /\.bed$/) {
  unlink $bedfile;
  croak "Error: file must contain .bed suffix";
}

my $operation = $q->param('operation');

(my $tlxbed = $tlxfile) =~ s/\.tlx$/.bed/;

System("/Users/robin/Scripts/tlx2BED.pl $tlxfile $tlxbed");



if ($operation eq "count") {
  my $output = $RESULT . basename($tlxfile,'.tlx') . "_count.bed";
  my $intersect_cmd = join(" ","bedtools intersect -c",
                               "-a $bedfile",
                               "-b $tlxbed",
                               "> $output");
  System($intersect_cmd);
} else {
  
  my $output = $RESULT . basename($tlxfile,'.tlx') . "_intersect.bed";

  my $intersect_cmd = join(" ","bedtools intersect",
                               $operation eq "extract" ? "-u" : "-v",
                               "-a $tlxbed",
                               "-b $bedfile",
                               "> $output");

  System($intersect_cmd);

  (my $tlxoutput = $output) =~ s/\.bed$/.tlx/;

  System("/Users/robin/Scripts/pullTLXFromBED.pl $tlxfile $output $tlxoutput");
  unlink $output;
}


print $q->p("Finished processing request.");
print $q->a({href=>"../results/"},"Download your results here.");

$q->end_html();

unlink $tlxfile;



BEGIN {
    carpout("STDOUT");
}


