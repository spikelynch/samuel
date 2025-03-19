use lib '.';
use Samuel;



$seed = (time ^ $$);

$fake = srand($seed);

$nstanza = 2 + int(rand($length / 2)) + int(rand($length / 2));




for( 1..$nstanza ) {
    $stanza = &stanza;
    $stanza =~ s/<br>/\n/g;
    print $stanza;
    if( $_ == $nstanza ) {
        print "\n";
    } else {
        print "\n\n";
    }
}


