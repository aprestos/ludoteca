<template>
  <!-- Modal -->
  <div>
    <b-modal
      :id="id"
      :hide-footer="hideFooter"
      :title="title"
      body-class="p-0"
      class=""
      scrollable
    >
      <template v-slot:modal-header>
        <slot name="header">
          <div class="input-group input-group-merge">
            <b-form-input
              v-model="search"
              class="form-control form-control-prepended search"
              debounce="300"
              flush
              placeholder="Search"
              type="search"
            />
            <div class="input-group-prepend">
              <div class="input-group-text">
                <b-icon-search font-scale="0.8"></b-icon-search>
              </div>
            </div>
          </div>
        </slot>
      </template>
      <template v-slot:default>
        <div style="min-height:400px; max-height: 400px">
          <slot name="content">
            <b-skeleton-wrapper :loading="loading">
              <template #loading>
                <b-list-group flush>
                <b-list-group-item class="px-4"
                >
                  <b-skeleton width="40%"/>
                </b-list-group-item>
          <b-list-group-item class="px-4"
                >
                  <b-skeleton width="60%"/>
                </b-list-group-item>
                            <b-list-group-item class="px-4"
                >
                  <b-skeleton width="20%"/>
                </b-list-group-item>

                            <b-list-group-item class="px-4"
                >
                  <b-skeleton width="70%"/>
                </b-list-group-item>
                                    <b-list-group-item class="px-4"
                >
                  <b-skeleton width="55%"/>
                </b-list-group-item>
                                    <b-list-group-item class="px-4"
                >
                  <b-skeleton width="25%"/>
                </b-list-group-item>
              </b-list-group>
              </template>
              <b-list-group flush>
                <b-list-group-item
                  v-for="(item, index) in itemList()"
                  v-bind:key="index"
                  button
                  class="px-4"
                  data-dismiss="modal"
                  @click="$emit('selected', item)"
                >
                  {{ item[itemTitle] }}
                  <span v-if="item[itemMetadata]" class="text-gray-600"
                    >({{ item[itemMetadata] }})</span
                  >
                </b-list-group-item>
                <b-list-group-item
                  v-show="items.length === 0"
                  class="px-4 text-muted"
                  >No results to show. Start typing to filter results
                </b-list-group-item>
              </b-list-group>
            </b-skeleton-wrapper>
          </slot>
        </div>
      </template>
      <template #modal-footer>
        <slot name="footer"></slot>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'ModalSelect',
  props: {
    id: String,
    title: String,
    hideFooter: {
      type: Boolean,
      default: false,
    },
    defaultItems: {
      type: Array
    },
    items: {
      type: Array,
    },
    itemTitle: {
      default: 'name',
    },
    itemMetadata: {},
    loading: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      search: '',
    }
  },
  watch: {
    search: function(val) {
      this.$emit('search', val)
    },
  },
  methods: {
    itemList(){
      return this.items && this.items.length ? this.items : this.defaultItems
      }
    }
}
</script>
