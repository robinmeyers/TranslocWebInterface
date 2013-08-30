#!/usr/bin/perl


use strict;
use warnings;
use CGI;
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
print $q->start_html("HTML Reads");
print $q->p("Processing Request...");

my $tlxfile = cgiUpload($q,'tlxfile',$UPLOAD);

unless ($tlxfile =~ /\.tlx$/) {
  unlink $tlxfile;
  croak "Error: file must contain .tlx suffix";
}


my $primer = $q->param('primer');
my $adapter = $q->param('adapter');
    
my ($path,$name,$ext) = parseFilename($tlxfile);
my $htmlfile = "$RESULT/$name.html";

my $syscmd = "/Users/robin/TranslocPipeline/bin/TranslocHTMLReads.pl $tlxfile $htmlfile";

$syscmd .= " --primer $primer" unless $primer eq "";
$syscmd .= " --adapter $adapter" unless $adapter eq "";

$ENV{'PATH'} .= ":/usr/local/bin";
print $q->p($ENV{'PATH'});

System("$syscmd") or croak "Error: failed executing the following command:<br>$syscmd<br>";

print $q->p("Finished processing request.");
print $q->a({href=>"../results/"},"Download your results here.");

$q->end_html();

unlink $tlxfile;



BEGIN {
    carpout("STDOUT");
}


