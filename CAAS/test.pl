use warnings;
use strict;
use File::Spec;

for ( @ARGV ) { 
    if ( -f ) {
        print File::Spec->rel2abs( $_ ), "\n";
    }   
}

