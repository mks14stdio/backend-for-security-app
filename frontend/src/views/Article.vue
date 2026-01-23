<template lang="">
    <AppHeader>Статьи</AppHeader>
    
    <div>
        <n-button @click="fetchData">Добавить новую статью</n-button>
    </div>
    <n-data-table
        :columns="columns"
        :data="data"
        :pagination="pagination"
        :bordered="true"
    />


</template>

<script lang="ts">
import AppHeader from "../components/AppHeader.vue"
import AppModuleList from "@/components/AppModuleList.vue";
import { articleService } from "@/api/service";

import { NButton } from "naive-ui";
import { NCard, NTabs, NTabPane } from "naive-ui";

const pagination = false as const;

import type {
    DataTableColumn,
    DataTableColumns,
    DataTableFilterState,
    DataTableSortOrder,
    DataTableSortState,
    PaginationInfo
} from 'naive-ui';
import { h } from "vue";

interface ArticleData {
    title: string | null;
    content: string;
    test_pk: number | null;
    id: number;
    created_at: string | null;
    updated_on: string | null;

};

const id_column: DataTableColumn<ArticleData> = {
    title: "ID",
    key: "id",
    width: 50
};

const title_column: DataTableColumn<ArticleData> = {
    title: "Заголовок",
    key: "title",
    width: 200
};

const created_at_column: DataTableColumn<ArticleData> = {
    title: "Дата создания",
    key: "created_at",
    width: 150
};

function createColumns({ edit_button } : { edit_button: (row: ArticleData) => void}): DataTableColumns<ArticleData> {
    const columns: DataTableColumns<ArticleData> = [
        id_column,
        title_column,
        created_at_column,
        {
            title: "Действия",
            key: "actions",
            width: 30,
            render(row) {
                return h(
                    NButton, {
                        type: "primary",
                        size: "small",
                        onClick: () => edit_button(row)
                    },
                    { default: () => "Редактировать" }
                );
            }
        }
    ];

    return columns;
}

const columns = createColumns({
    edit_button: (row: ArticleData) => {
        console.log("Edit article:", row);
    }
});

export default {

    methods: {
        async fetchData() {
            try {
                const responce = await articleService.get_all(10, 0); 
                this.article_data = responce;
            } catch(e) {
                console.log(e);
            }
        }
    },

    components: {
        AppHeader,
        AppModuleList,
        NButton, NCard, NTabs, NTabPane, DataTableColumns
    },


    mounted() {
        (async () => {
            try {
                await this.fetchData();
            } catch (error) {
                console.error(error);
            }
        })();
    },
    

    data() {
        return {
            article_data: [] as ArticleData[],
        }
    }
}
</script>

<style></style>