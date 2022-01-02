# use Test2::V0;
use Test2::Bundle::More;



use Data::Printer;
use ok 'Vote::ABIF';

my $test012 = Vote::ABIF->new( fileIn => 'testfiles/test012.abif' );
$test012->parse();
is_deeply( $test012->metadata, {},
  'file without ABIF header and only choices list generates only generates choices list' );

# metadata after ballots


# my $test012A = Vote::ABIF->new( fileIn => 'testfiles/test012_headerA.abif' );
# $test012A->parse();
# is_deeply( $test012A->metadata, {},
#   'file with ABIF header and no version or metadata has empty metadata' );

# my $test012B = Vote::ABIF->new( fileIn => 'testfiles/test012_headerB.abif' );
# $test012B->parse();
# is_deeply( $test012B->metadata, { 'version' => '1.0' },
#   'file with ABIF header and just the version has only versiopn in  meteadata' );

# my $test012C = Vote::ABIF->new( fileIn => 'testfiles/test012_headerC.abif' );
# $test012C->parse();
# is_deeply( $test012C->metadata, { 'ballot_type' => 'ordinal', 'version' => '1.0' },
#   'file with ABIF header and json has meteadata' );


done_testing();
