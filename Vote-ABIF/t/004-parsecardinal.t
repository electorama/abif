# use Test2::V0;
use Test2::Bundle::More;

use Data::Printer;

use Vote::ABIF;

my $test1 = Vote::ABIF->new( fileIn => 'testfiles/test001.abif' );

my %lines = (
  27 => q|27: [Doña García Márquez] > SBJ > [Fay Wray] > AM|,
  26 => q|26 : SBJ >[Doña García Márquez] = SY> AM|,
  25 => q|22: [Collins, Josette] = [Stoddard-Collins, Caroline] > [Trask: Elias/Lamar/Gregory]|,
  24 => q|24: SY > DGM = AM > SBJ|,
  23 => q|23: AM > SY > SBJ > [Doña García Márquez]  > [Fay Wray]  |,
  22 => q|22: SBJ |,
);

subtest '_ordinalline Parising Ordinal Ballot Lines' => sub {
my $r25 =  $test1->_ordinalline( $lines{ 25 } ) ;
p $r25;
  is_deeply(
    $test1->_ordinalline( $lines{ 27 } ),
    { 'count' => 27, 'Doña García Márquez' => -1, 'SBJ' => -2, 'Fay Wray' => -3, 'AM' => -4 },
    "$lines{ 27 }"
  );
  is_deeply(
    $test1->_ordinalline( $lines{ 26 } ),
    { 'count' => 26, 'Doña García Márquez' => -2, 'SBJ' => -1, 'SY' => -2, 'AM' => -3 },
    "$lines{ 26 }"
  );
  is_deeply(
    $test1->_ordinalline( $lines{ 24 } ),
    { 'count' => 24, 'DGM' => -2, 'SBJ' => -3, 'SY' => -1, 'AM' => -2 },
    "$lines{ 24 }"
  );
  is_deeply(
    $test1->_ordinalline( $lines{ 23 } ),
    { 'count' => 23,
      'Doña García Márquez' => -4, 'SBJ' => -3, 'SY' => -2, 'AM' => -1, 'Fay Wray' => -5 },
    "$lines{ 23 }"
  );
  is_deeply(
    $test1->_ordinalline( $lines{ 22 } ),
    { 'count' => 22, 'SBJ' => -1 },
    "$lines{ 22 }"
  );
};

# my $test012 = Vote::ABIF->new( fileIn => 'testfiles/test012.abif' );
# $test012->parse();
# is_deeply( $test012->metadata, {},
#   'file without ABIF header and only choices list generates only generates choices list' );

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
