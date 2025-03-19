use lib '.';
use CGI;
use Samuel;


$query = CGI->new;

&start_page;

$seed = $query->param('s') || (time ^ $$);

$fake = srand($seed);

$nstanza = 2 + int(rand($length / 2)) + int(rand($length / 2));


for( 1..$nstanza ) {
    print "<p>" . &stanza . "</p>\n";
}


&end_page($seed);
