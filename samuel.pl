use lib '/home/mike/bots/samuel/';
use Samuel;
use Bot;
use JSON;


my $CONFIG_FILE = '/home/mike/bots/samuel/samuel_at.json';

sub poem {

    $seed = (time ^ $$);

    $fake = srand($seed);

    $nstanza = 2 + int(rand($length / 2)) + int(rand($length / 2));

    $poem = '';
    for( 1..$nstanza ) {
        $stanza = &stanza;
        $stanza =~ s/<br>/\n/g;
        $poem .= $stanza;
        if( $_ == $nstanza ) {
            $poem .= "\n";
        } else {
            $poem .= "\n\n";
        }
    }
    $poem;
}

sub load_config {
    my ( $config ) = @_;
    my $json_text = do {
       open(my $json_fh, "<:encoding(UTF-8)", $config)
          or die("Can't open \"$config\": $!\n");
       local $/;
       <$json_fh>
    };

    my $json = JSON->new;
    $json->decode($json_text);
}

my $cf = &load_config($CONFIG_FILE);

my $bot = Bot->new($cf->{base_url}, $cf->{access_token});

my $verses = &poem;

$bot->post($verses, $cf->{content_warning});

