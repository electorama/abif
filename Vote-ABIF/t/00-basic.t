use Test2::V0;

use ok 'Vote::ABIF';

my $test1 = Vote::ABIF->new( fileIn => 'testfiles/test001.abif' );
ok( $test1, 'successful creation of object' );
isa_ok( $test1, 'Vote::ABIF' );
can_ok( $test1, 'fileIn' );
can_ok( $test1, 'ballotType' );
can_ok( $test1, 'ballotTypeForce' );

done_testing();
