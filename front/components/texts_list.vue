<template>

  <v-card
    style="height: 100%"
  >
    <v-sheet class="pa-4 gradient-lighten lighten-2 d-flex flex-row">
      <v-text-field
        v-model="search"
        label="Search"
        dark
        flat
        solo-inverted
        hide-details
        clear-icon="mdi-close-circle-outline"
      ></v-text-field>
      <v-btn icon class="mt-2 ml-2" @click="creatingDialog=!creatingDialog">
        <v-icon large>mdi-plus-circle-outline</v-icon>
      </v-btn>
    </v-sheet>
    <v-card-text>
      <v-responsive class="overflow-y-auto" max-height="75vh">
        <v-card
          v-for="(text, idx) in filteredTexts"
          :key="idx"
          color="#385F73"
          dark
          class="mb-2"
        >
          <v-card-title class="headline">
            <v-btn icon @click="removeTextId=text.id; removingDialog=!removingDialog">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
            <v-btn icon @click="updateTextId=text.id; updateTextTitle=text.title; updateTextText=text.default_text; updatingDialog=!updatingDialog">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            {{text.title}}
          </v-card-title>

          <v-card-subtitle style="font-size: small">{{text.default_text}}</v-card-subtitle>

        </v-card>
      </v-responsive>
    </v-card-text>

    <!--    Removing dialog-->
    <v-dialog
      v-model="removingDialog"
      persistent
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
           Удаление Text
        </v-card-title>
        <v-card-text>Вы уверены?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red darken-1"
            text
            @click="removingDialog = false; removeText()"
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
<!--    Creating dialog-->
    <v-dialog
        v-model="creatingDialog"
        max-width="500px"
      >
        <v-card>
          <v-card-title>
            Добавить Text
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="newTextTitle" label="Title"></v-text-field>
            <v-textarea v-model="newTextText" placeholder="Text" label="Text"/>
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
              @click="createNewText"
            >
              Create
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
<!--    Updating dialog-->
      <v-dialog
          v-model="updatingDialog"
          max-width="500px"
        >
        <v-card>
          <v-card-title>
            Изменить Text
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="updateTextTitle" label="Title"></v-text-field>
            <v-textarea v-model="updateTextText" label="Text"/>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              text
              @click="updatingDialog = false"
            >
              Close
            </v-btn>
            <v-btn
              color="warning"
              text
              @click="updateText"
            >
              Update
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-card>
</template>

<script>
    export default {
      props: {
        texts: Array,
        group: String
      },
      data: () => ({
        search: "",

        creatingDialog: false,
        newTextTitle: null,
        newTextText: null,

        updatingDialog: false,
        updateTextId: null,
        updateTextTitle: null,
        updateTextText: null,

        removingDialog: false,
        removeTextId: null
      }),
      computed: {
        filteredTexts () {
          return this.texts.filter(item => item.default_text.indexOf(this.search) > -1 && !item.is_hint)
        },
      },
      methods: {
        createNewText() {
          this.$axios.post(
            '/quiz/messages/',
            {
              title: this.newTextTitle,
              default_text: this.newTextText
            }
          )
            .then(response => {
              this.newTextTitle = null
              this.newButtonText = null
              this.$store.dispatch("components/setTexts")
            })

          this.creatingDialog = false
        },
        removeText() {
          this.$axios.delete(
            "/quiz/messages/" + this.removeTextId
          )
            .then(response => {
              this.$store.dispatch("components/setTexts")
            })
        },
        updateText() {
          this.$axios.put(
            "/quiz/messages/" + this.updateTextId + "/",
            {
              title: this.updateTextTitle,
              default_text: this.updateTextText
            }
          )
            .then(response => {
              this.updateTextId = null
              this.newTextTitle = null
              this.newButtonText = null
              this.$store.dispatch("components/setTexts")
            })
          this.updatingDialog = false
        }
      }
  }
</script>

<style scoped>

</style>
