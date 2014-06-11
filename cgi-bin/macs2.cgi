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
print $q->start_html("MACS2");
print $q->p("Processing Request...");
my $tlxfile = cgiUpload($q,'tlxfile',$UPLOAD);

unless ($tlxfile =~ /\.tlx$/) {
  unlink $tlxfile;
  croak "Error: file must contain .tlx suffix";
}

my $genome = $q->param('genome');
my $extsize = $q->param('extsize');
my $largelocal = $q->param('largelocal');
my $qvalueexp = $q->param('qvalue');
my $qvalue = 10**(-$qvalueexp);


my ($path,$name,$ext) = parseFilename($tlxfile);
my $bedfile = "$RESULT/$name.bed";

my $bed_cmd = "/Users/robin/Scripts/tlx2BED-MACS.pl $tlxfile $bedfile $extsize";
System($bed_cmd) or croak "Error: $bed_cmd";


my $macs_cmd = "/usr/local/bin/macs2 callpeak -t $bedfile -f BED -g $genome --keep-dup all -n $RESULT/$name --nomodel --extsize $extsize -q $qvalue --llocal $largelocal";
System($macs_cmd) or croak "Error: $macs_cmd";

print $q->p("Finished processing request.");
print $q->a({href=>"../results/"},"Download your results here.");

$q->end_html();

unlink $tlxfile;



BEGIN {
    carpout("STDOUT");
}


