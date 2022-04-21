#include <iostream>
#include <vdb/manager.h>
#include <vdb/database.h>
#include <vdb/table.h>
#include <vdb/cursor.h>

int main() {
    const char *file_name = "../../SRR.sra";
    const VDBManager *mgr = 0;
    const VDatabase *db = 0;
    KNamelist *namelist = 0;
    const char* tablename;

    VDBManagerMakeRead(&mgr, 0);
    VDBManagerOpenDBRead(mgr, &db, 0, file_name);

    VDatabaseListTbl(db, &namelist);
    uint32_t count = 0;
    KNamelistCount ( namelist, &count );
//    std::cout << "File " << file_name << " contains the following tables:" << std::endl;
    for (uint32_t c = 0; c < count; ++c ) {
        KNamelistGet ( namelist, 0, &tablename);
//        std::cout << "    " << tablename << std::endl;
        const VTable *seq_table = 0;
        VDatabaseOpenTableRead(db, &seq_table, tablename);
        const VCursor* seq_cursor = 0;
        VTableCreateCursorRead(seq_table, &seq_cursor);
        VCursorRelease(seq_cursor);
        VTableRelease(seq_table);
    }

    KNamelistRelease(namelist);
    VDatabaseRelease(db);
    VDBManagerRelease(mgr);

    std::cout << "NCBI-VDB package is ready" <<std::endl;
}
