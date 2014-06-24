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

my $output = $q->param('output');
$output =~ s/[^$safe_chars]/_/g;
croak "Error: please name your file" unless $output =~ /\S/;

my $readfile = cgiUpload($q,'readfile',$UPLOAD);

unless ($readfile =~ /\.txt$/) {
  unlink $readfile;
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
my $filtstart = $q->param('filtstart');
my $filtend = $q->param('filtend');
my $minsubs = $q->param('minsubs');
my $maxsubs = $q->param('maxsubs');
my $mindels = $q->param('mindels');
my $maxdels = $q->param('maxdels');
my $minins = $q->param('minins');
my $maxins = $q->param('maxins');

my $rmdups = defined $q->param('rmdups') ? "T" : "F";



my $shmprofile_cmd = join(" ","Rscript",
                              "/Users/robin/SHMPipeline/R/SHMProfile.R",
                              "$mutfile $readfile $refseqfile $RESULT/$output",
                              "tstart=$tstart tend=$tend",
                              "filtstart=$filtstart filtend=$filtend",
                              "minsubs=$minsubs maxsubs=$maxsubs",
                              "mindels=$mindels maxdels=$maxdels",
                              "minins=$minins minins=$minins",
                              "rmdups=$rmdups");
System($shmprofile_cmd) or croak "Error: $shmprofile_cmd";

print $q->p("Finished processing request.");
print $q->a({href=>"../results/"},"Download your results here.");

$q->end_html();

unlink $readfile;
unlink $mutfile;
unlink $refseqfile;



BEGIN {
    carpout("STDOUT");
}


