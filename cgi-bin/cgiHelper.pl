#!/usr/bin/perl

use strict;
use warnings;
use Carp;
use File::Basename;
use IO::Handle;
use IO::File;
use CGI;




#invert exit status of system call
sub System {
    my $cmd = shift;
    print "$cmd\n";
    my $status = system($cmd);
    return !$status;
}

sub parseFilename {
    my $fullname = shift;
    my ($name, $path, $ext) = fileparse($fullname, qr/\.\w{2,5}$/);
    return ($path, $name, $ext);
}

sub cgiUpload {
    my $cgi = shift;
    my $param = shift;
    my $outdir = shift;
    my $safe_chars =  "A-Za-z0-9_.-";
    my $file = $cgi->param($param);
    return undef unless $file;
    my ($path,$name,$ext) = parseFilename($file);
    $file = $name.$ext;
    $file =~ s/ /_/g;
    $file =~ s/[^$safe_chars]//g;
    $file = $outdir.$file;
    print $cgi->p("Uploading file to server at $file...");

    my $fh  = $cgi->upload($param);
    if (defined $fh) {
        # Upgrade the handle to one compatible with IO::Handle:
        my $io_handle = $fh->handle;
        open OUTFILE,">",$file or croak "Error: could not open $file for writing";
        while (my $bytesread = $io_handle->read(my $buffer,1024)) {
            print OUTFILE $buffer;
        }
    }
    System("perl -pi -e 's/\r/\n/g' $file");

    return $file;
}


1;
