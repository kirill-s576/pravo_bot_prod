<template>
  <v-card
    style="height: 100%"
  >
    <v-sheet class="pa-4 gradient-lighten lighten-2">
      <v-text-field
        v-model="search"
        label="Search"
        dark
        flat
        solo-inverted
        hide-details
        clearable
        clear-icon="mdi-close-circle-outline"
      ></v-text-field>
    </v-sheet>
    <v-card-text>
      <v-responsive class="overflow-y-auto overflow-x-auto" max-height="75vh">
        <v-treeview
          :items="stagesTree"
          :search="search"
          :filter="filter"
          :item-text="'title'"
          activatable
          hoverable
          shaped
          dense
          :open.sync="open"
          :active.sync="mdl"
        >
          <template v-slot:prepend="{ item }">
            <v-icon
              v-if="item.children"
              v-text="`mdi-${item.id === 1 ? 'home-variant' : 'folder-network'}`"
            ></v-icon>
          </template>
          <template v-slot:label="{item}">
            <div v-if="!item.removed">
               {{ item.button }} --> {{item.title}}
            </div>
            <div v-else style="color: orangered">
              REMOVED
            </div>

          </template>
          <template v-slot:append="{item}">
            <v-btn @click="removingStage = item; removingDialog = true;" icon>
              <v-icon>mdi-delete</v-icon>
            </v-btn>
            <v-btn icon>
              <v-icon @click="creatingDialog=true; newStageToStage=item">mdi-plus-circle</v-icon>
            </v-btn>
          </template>
        </v-treeview>
      </v-responsive>
    </v-card-text>

    <v-dialog
      v-model="removingDialog"
      persistent
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
           Удаление Stage
        </v-card-title>
        <v-card-text>Вы уверены?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="removingDialog = false; deleteStage(removingStage)"
          >
            Да
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="removingDialog = false"
          >
            Нет
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
        v-model="creatingDialog"
        max-width="500px"
      >
        <v-card>
          <v-card-title>
            Создание нового Stage
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="newStageTitle" label="Title"></v-text-field>
            <v-select
              v-model="newStageButtonId"
              :items="buttons"
              item-text="default_text"
              item-value="id"
              label="A Select List"
            ></v-select>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              text
              @click="creatingDialog = false"
            >
              Close
            </v-btn>
            <v-btn
              color="success"
              text
              @click="createEmptyStage"
            >
              Create
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-card>
</template>

<script>
  export default {
    props: {
      stagesTree: Array
    },
    data: () => ({
      items: [
      ],
      mdl: [],
      open: [],
      search: null,
      caseSensitive: false,
      removingDialog: false,
      removingStage: null,
      creatingDialog: false,
      newStageToStage: null,
      newStageButtonId: null,
      newStageTitle: null
    }),
    computed: {
      filter() {
        return this.caseSensitive
          ? (item, search, textKey) => item[textKey].indexOf(search) > -1
          : undefined
      },
      buttons () {
        return this.$store.getters["components/getButtons"]
      }
    },
    watch: {
      mdl (newValue) {
        if ( newValue[0] ) {
          this.$emit("emptyStageCreated", newValue[0])
        }
      }
    },
    methods: {
      createEmptyStage () {
        this.$axios.post(
          "/quiz/stages/",
          {
            to_stage_id: this.newStageToStage.id,
            title: this.newStageTitle,
            button_id: this.newStageButtonId
          }
        )
        .then(response => {
          this.newStageToStage.children.push(response.data)
          this.creatingDialog = false
          this.$emit("emptyStageCreated", response.data.id)
        })
      },
      deleteStage( stage ) {
        this.$axios.delete(
          "/quiz/stages/" + stage.id
        )
          .then(response => {
            stage.removed = true
          })
      }
    }
  }
</script>

<style scoped>

</style>
