use Test2::V0;

use ok 'Vote::ABIF';

my $test1 = Vote::ABIF->new( fileIn => 'testfiles/test001.abif' );
ok( $test1, 'successful creation of object' );
isa_ok( $test1, 'Vote::ABIF' );
for my $method ( qw( parse metadata _parseABIFHead _parseMetaData _validateMetaData)) {
  can_ok( $test1, $method) ;
}

is( $test1->{'currentlist'}, 'choices', 'current list defaulted to choices' );
is( $test1->{'finishedmetadata'}, 0, 'finishedmetadata is defaulted to 0' );
is( $test1->{'fileIn'}, "testfiles/test001.abif", 'filein is set in object' );

done_testing();
